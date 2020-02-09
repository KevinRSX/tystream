/* -*-mode:c++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */

#include <thread>
#include <chrono>

#include <sys/socket.h>
#include <net/route.h>

#include "packetshell.hh"
#include "netdevice.hh"
#include "nat.hh"
#include "util.hh"
#include "interfaces.hh"
#include "address.hh"
#include "dns_server.hh"
#include "timestamp.hh"
#include "exception.hh"
#include "bindworkaround.hh"
#include "config.h"

#include <netinet/in.h> 
#include <string.h> 
#include "signalfd.hh"
using namespace std;
using namespace PollerShortNames;

template <class FerryQueueType>
PacketShell<FerryQueueType>::PacketShell( const std::string & device_prefix, char ** const user_environment )
    : user_environment_( user_environment ),
      egress_ingress( two_unassigned_addresses( get_mahimahi_base() ) ),
      nameserver_( first_nameserver() ),
      egress_tun_( device_prefix + "-" + to_string( getpid() ) , egress_addr(), ingress_addr() ),
      dns_outside_( egress_addr(), nameserver_, nameserver_ ),
      nat_rule_( ingress_addr() ),
      pipe_( UnixDomainSocket::make_pair() ),
      event_loop_()
{
    /* make sure environment has been cleared */
    if ( environ != nullptr ) {
        throw runtime_error( "PacketShell: environment was not cleared" );
    }

    /* initialize base timestamp value before any forking */
    //initial_timestamp();
}

template <class FerryQueueType>
template <typename... Targs>
void PacketShell<FerryQueueType>::start_uplink( const string & shell_prefix,
                                                const vector< string > & command,
                                                Targs&&... Fargs )
{
    /* g++ bug 55914 makes this hard before version 4.9 */
    BindWorkAround::bind<FerryQueueType, Targs&&...> ferry_maker( forward<Targs>( Fargs )... );

    /*
      This is a replacement for expanding the parameter pack
      inside the lambda, e.g.:

    auto ferry_maker = [&]() {
        return FerryQueueType( forward<Targs>( Fargs )... );
    };
    */

    /* Fork */
    event_loop_.add_special_child_process( 77, "packetshell", [&]() {
			
            TunDevice ingress_tun( "ingress", ingress_addr(), egress_addr() );
            /* bring up localhost */
            interface_ioctl( SIOCSIFFLAGS, "lo",
                             [] ( ifreq &ifr ) { ifr.ifr_flags = IFF_UP; } );

            /* create default route */
            rtentry route;
            zero( route );

            route.rt_gateway = egress_addr().to_sockaddr();
            route.rt_dst = route.rt_genmask = Address().to_sockaddr();
            route.rt_flags = RTF_UP | RTF_GATEWAY;

            SystemCall( "ioctl SIOCADDRT", ioctl( UDPSocket().fd_num(), SIOCADDRT, &route ) );

            Ferry inner_ferry;

            /* dnsmasq doesn't distinguish between UDP and TCP forwarding nameservers,
               so use a DNSProxy that listens on the same UDP and TCP port */

            UDPSocket dns_udp_listener;
            dns_udp_listener.bind( ingress_addr() );

            TCPSocket dns_tcp_listener;
            dns_tcp_listener.bind( dns_udp_listener.local_address() );

            DNSProxy dns_inside_ { move( dns_udp_listener ), move( dns_tcp_listener ),
                    dns_outside_.udp_listener().local_address(),
                    dns_outside_.tcp_listener().local_address() };

            dns_inside_.register_handlers( inner_ferry );

            /* run dnsmasq as local caching nameserver */
            inner_ferry.add_child_process( start_dnsmasq( {
                        "-S", dns_inside_.udp_listener().local_address().str( "#" ) } ) );

            /* Fork again after dropping root privileges */
            drop_privileges();

            /* restore environment */
            environ = user_environment_;

            /* set MAHIMAHI_BASE if not set already to indicate outermost container */
            SystemCall( "setenv", setenv( "MAHIMAHI_BASE",
                                          egress_addr().ip().c_str(),
                                          false /* don't override */ ) );

            inner_ferry.add_child_process( join( command ), [&]() {
                    /* tweak bash prompt */
                    prepend_shell_prefix( shell_prefix );

                    return ezexec( command, true );
                } );
            /* allow downlink to write directly to inner namespace's TUN device */
            pipe_.first.send_fd( ingress_tun );

            FerryQueueType uplink_queue { ferry_maker() };
            //return inner_ferry.loop( uplink_queue, ingress_tun, egress_tun_ );
            /*int server_fd, new_socket, valread; 
            struct sockaddr_in address; 
            int opt = 1; 
            int addrlen = sizeof(address); 
            char buffer[1024] = {0}; 
       
            // Creating socket file descriptor 
            if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) 
            { 
                perror("socket failed"); 
                exit(EXIT_FAILURE); 
            } 
       
            // Forcefully attaching socket to the port 8080 
            if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 
                                                  &opt, sizeof(opt))) 
            { 
                perror("setsockopt"); 
                exit(EXIT_FAILURE); 
            } 
            address.sin_family = AF_INET; 
            address.sin_addr.s_addr = INADDR_ANY; 
            address.sin_port = htons(8080); 
       
            // Forcefully attaching socket to the port 8080 
            if (bind(server_fd, (struct sockaddr *)&address,  
                                 sizeof(address))<0) 
            { 
                perror("bind failed"); 
                exit(EXIT_FAILURE); 
            } 
            if (listen(server_fd, 3) < 0) 
            { 
                perror("listen"); 
                exit(EXIT_FAILURE); 
            } 
            if ((new_socket = accept(server_fd, (struct sockaddr *)&address,  
                       (socklen_t*)&addrlen))<0) 
            { 
                perror("accept"); 
                exit(EXIT_FAILURE); 
            } 
            while(true){
                valread = read( new_socket , buffer, 1024); 
                printf("%s\n", buffer); 
                printf("%d\n", valread);
                printf("%d\n", strcmp(buffer, "ok"));
                if(strcmp(buffer, "ok") < 0){
                    break;
                }
            } 
            close(new_socket);*/
	    return inner_ferry.loop( uplink_queue, ingress_tun, egress_tun_ );
        }, true );  /* new network namespace */
}

template <class FerryQueueType>
template <typename... Targs>
void PacketShell<FerryQueueType>::start_downlink( Targs&&... Fargs )
{
    /* g++ bug 55914 makes this hard before version 4.9 */
    BindWorkAround::bind<FerryQueueType, Targs&&...> ferry_maker( forward<Targs>( Fargs )... );

    /*
      This is a replacement for expanding the parameter pack
      inside the lambda, e.g.:

    auto ferry_maker = [&]() {
        return FerryQueueType( forward<Targs>( Fargs )... );
    };
    */

    event_loop_.add_special_child_process( 77, "downlink", [&] () {
	    drop_privileges();
            /* restore environment */
            environ = user_environment_;

            /* downlink packets go to inner namespace's TUN device */
            FileDescriptor ingress_tun = pipe_.second.recv_fd();
            Ferry outer_ferry;

            dns_outside_.register_handlers( outer_ferry );

            FerryQueueType downlink_queue { ferry_maker() };
            /*int server_fd, new_socket, valread; 
	    struct sockaddr_in address; 
	    int opt = 1; 
	    int addrlen = sizeof(address); 
	    char buffer[1024] = {0}; 
       
	    // Creating socket file descriptor 
	    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) 
	    { 
		perror("socket failed"); 
		exit(EXIT_FAILURE); 
	    } 
       
	    // Forcefully attaching socket to the port 8080 
	    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 
                                                  &opt, sizeof(opt))) 
	    { 
		perror("setsockopt"); 
		exit(EXIT_FAILURE); 
	    } 
	    address.sin_family = AF_INET; 
	    address.sin_addr.s_addr = INADDR_ANY; 
	    address.sin_port = htons(8080); 
       
	    // Forcefully attaching socket to the port 8080 
	    if (bind(server_fd, (struct sockaddr *)&address,  
                                 sizeof(address))<0) 
	    { 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	    } 
	    if (listen(server_fd, 3) < 0) 
	    { 
		perror("listen"); 
		exit(EXIT_FAILURE); 
	    } 
	    if ((new_socket = accept(server_fd, (struct sockaddr *)&address,  
                       (socklen_t*)&addrlen))<0) 
	    { 
		perror("accept"); 
		exit(EXIT_FAILURE); 
	    } 
	    while(true){
		valread = read( new_socket , buffer, 1024); 
		printf("%s\n", buffer); 
		printf("%d\n", valread);
		printf("%d\n", strcmp(buffer, "ok"));
		if(strcmp(buffer, "ok") < 0){
		    break;
		}
	    } 
	    close(new_socket);*/
            //return outer_ferry.loop(downlink_queue, egress_tun_, ingress_tun);
	    outer_ferry.loop(downlink_queue, egress_tun_, ingress_tun);
	    return -1;
	    /*int server_fd, new_socket, valread;
            struct sockaddr_in address;
            int opt = 1;
            int addrlen = sizeof(address);
            char buffer[1024] = {0};
	    printf("%s\n", "HELLO");

            // Creating socket file descriptor
            if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
            {
                perror("socket failed");
                exit(EXIT_FAILURE);
            }

            // Forcefully attaching socket to the port 8080
            if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
                                                  &opt, sizeof(opt)))
            {
                perror("setsockopt");
                exit(EXIT_FAILURE);
            }
            address.sin_family = AF_INET;
            address.sin_addr.s_addr = INADDR_ANY;
            address.sin_port = htons(8080);

            // Forcefully attaching socket to the port 8080
            if (bind(server_fd, (struct sockaddr *)&address,
                                 sizeof(address))<0)
            {
                perror("bind failed");
                exit(EXIT_FAILURE);
            }
            if (listen(server_fd, 3) < 0)
            {
                perror("listen");
                exit(EXIT_FAILURE);
            }
            if ((new_socket = accept(server_fd, (struct sockaddr *)&address,
                       (socklen_t*)&addrlen))<0)
            {
                perror("accept");
                exit(EXIT_FAILURE);
            }
            while(true){
                valread = read( new_socket , buffer, 1024);
                printf("%s\n", buffer);
                printf("%d\n", valread);
                printf("%d\n", strcmp(buffer, "ok"));
                if(strcmp(buffer, "ok") < 0){
                    break;
                }
            }
            close(server_fd);*/
	    //return downlink_queue.finished();
        } );
        sleep(4.5);
	//SignalFD signal_fd(SIGINT);
        //printf("start new:%s\n", "new");
	//initial_timestamp();
        event_loop_.add_special_child_process( 77, "downlink", [&] () {
            drop_privileges();
            /* restore environment */
            environ = user_environment_;

            /* downlink packets go to inner namespace's TUN device */
            FileDescriptor ingress_tun = pipe_.second.recv_fd();
            Ferry outer_ferry;

            dns_outside_.register_handlers( outer_ferry );

            FerryQueueType downlink_queue { ferry_maker() };
            /*int server_fd, new_socket, valread; 
            struct sockaddr_in address; 
            int opt = 1; 
            int addrlen = sizeof(address); 
            char buffer[1024] = {0}; 
       
            // Creating socket file descriptor 
            if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) 
            { 
                perror("socket failed"); 
                exit(EXIT_FAILURE); 
            } 
       
            // Forcefully attaching socket to the port 8080 
            if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 
                                                  &opt, sizeof(opt))) 
            { 
                perror("setsockopt"); 
                exit(EXIT_FAILURE); 
            } 
            address.sin_family = AF_INET; 
            address.sin_addr.s_addr = INADDR_ANY; 
            address.sin_port = htons(8080); 
       
            // Forcefully attaching socket to the port 8080 
            if (bind(server_fd, (struct sockaddr *)&address,  
                                 sizeof(address))<0) 
            { 
                perror("bind failed"); 
                exit(EXIT_FAILURE); 
            } 
            if (listen(server_fd, 3) < 0) 
            { 
                perror("listen"); 
                exit(EXIT_FAILURE); 
            } 
            if ((new_socket = accept(server_fd, (struct sockaddr *)&address,  
                       (socklen_t*)&addrlen))<0) 
            { 
                perror("accept"); 
                exit(EXIT_FAILURE); 
            } 
            while(true){
                valread = read( new_socket , buffer, 1024); 
                printf("%s\n", buffer); 
                printf("%d\n", valread);
                printf("%d\n", strcmp(buffer, "ok"));
                if(strcmp(buffer, "ok") < 0){
                    break;
                }
            } 
            close(server_fd);*/
            return outer_ferry.loop(downlink_queue, egress_tun_, ingress_tun);
        } );
	initial_timestamp();

}

// start_downlink1
template <class FerryQueueType>
template <typename... Targs>
void PacketShell<FerryQueueType>::start_downlink_1( Targs&&... Fargs )
{
    /* g++ bug 55914 makes this hard before version 4.9 */
    BindWorkAround::bind<FerryQueueType, Targs&&...> ferry_maker( forward<Targs>( Fargs )... );

    /*
      This is a replacement for expanding the parameter pack
      inside the lambda, e.g.:

    auto ferry_maker = [&]() {
        return FerryQueueType( forward<Targs>( Fargs )... );
    };
    */

    event_loop_.add_special_child_process( 77, "downlink_1", [&] () {
	    drop_privileges();
            /* restore environment */
            environ = user_environment_;

            /* downlink packets go to inner namespace's TUN device */
            FileDescriptor ingress_tun = pipe_.second.recv_fd();
            Ferry outer_ferry;

            dns_outside_.register_handlers( outer_ferry );

            FerryQueueType downlink_queue { ferry_maker() };
            int server_fd, new_socket, valread; 
	    struct sockaddr_in address; 
	    int opt = 1; 
	    int addrlen = sizeof(address); 
	    char buffer[1024] = {0}; 
       
	    // Creating socket file descriptor 
	    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) 
	    { 
		perror("socket failed"); 
		exit(EXIT_FAILURE); 
	    } 
       
	    // Forcefully attaching socket to the port 8080 
	    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 
                                                  &opt, sizeof(opt))) 
	    { 
		perror("setsockopt"); 
		exit(EXIT_FAILURE); 
	    } 
	    address.sin_family = AF_INET; 
	    address.sin_addr.s_addr = INADDR_ANY; 
	    address.sin_port = htons(8080); 
       
	    // Forcefully attaching socket to the port 8080 
	    if (bind(server_fd, (struct sockaddr *)&address,  
                                 sizeof(address))<0) 
	    { 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	    } 
	    if (listen(server_fd, 3) < 0) 
	    { 
		perror("listen"); 
		exit(EXIT_FAILURE); 
	    } 
	    if ((new_socket = accept(server_fd, (struct sockaddr *)&address,  
                       (socklen_t*)&addrlen))<0) 
	    { 
		perror("accept"); 
		exit(EXIT_FAILURE); 
	    } 
	    while(true){
		valread = read( new_socket , buffer, 1024); 
		printf("%s\n", buffer); 
		printf("%d\n", valread);
		printf("%d\n", strcmp(buffer, "ok"));
		if(strcmp(buffer, "ok") < 0){
		    break;
		}
	    } 
	    close(new_socket);
            return outer_ferry.loop(downlink_queue, egress_tun_, ingress_tun);
        } );

}


template <class FerryQueueType>
int PacketShell<FerryQueueType>::wait_for_exit( void )
{
    return event_loop_.loop();
}

template <class FerryQueueType>
int PacketShell<FerryQueueType>::Ferry::loop( FerryQueueType & ferry_queue,
                                              FileDescriptor & tun,
                                              FileDescriptor & sibling )
{
    /* tun device gets datagram -> read it -> give to ferry */
    add_simple_input_handler( tun, 
                              [&] () {
                                  ferry_queue.read_packet( tun.read() );
                                  return ResultType::Continue;
                              } );

    /* ferry ready to write datagram -> send to sibling's tun device */
    add_action( Poller::Action( sibling, Direction::Out,
                                [&] () {
                                    ferry_queue.write_packets( sibling );
                                    return ResultType::Continue;
                                },
                                [&] () { return ferry_queue.pending_output(); } ) );

    /* exit if finished */
    add_action( Poller::Action( sibling, Direction::Out,
                                [&] () {
                                    return Result( ResultType::Exit, 77 );
                                },
                                [&] () { return ferry_queue.finished(); } ) );

    return internal_loop( [&] () { return ferry_queue.wait_time(); } );
}

struct TemporaryEnvironment
{
    TemporaryEnvironment( char ** const env )
    {
        if ( environ != nullptr ) {
            throw runtime_error( "TemporaryEnvironment: cannot be entered recursively" );
        }
        environ = env;
    }

    ~TemporaryEnvironment()
    {
        environ = nullptr;
    }
};

template <class FerryQueueType>
Address PacketShell<FerryQueueType>::get_mahimahi_base( void ) const
{
    /* temporarily break our security rule of not looking
       at the user's environment before dropping privileges */
    TemporarilyUnprivileged tu;
    TemporaryEnvironment te { user_environment_ };

    const char * const mahimahi_base = getenv( "MAHIMAHI_BASE" );
    if ( not mahimahi_base ) {
        return Address();
    }

    return Address( mahimahi_base, 0 );
}
