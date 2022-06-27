import argparse
import yaml
import requests
import ast
import bjointsp.main as bjointsp
from place_emu.placement import random_placement, greedy_placement, random_placement2
from util.writer import write_placement2

compute_url = 'http://127.0.0.1:5001/restapi/compute/'
network_url = 'http://127.0.0.1:5001/restapi/network'
config_prefix = " -H 'Content-Type: application/json' -d "

def emulate_placement(placement):
    with open(placement, 'r') as place_file:
        result = yaml.load(place_file,Loader=yaml.FullLoader)
        # start placed VNF instances on the emulator
        for vnf in result['placement']['vnfs']:
            data = ast.literal_eval(vnf['image'])      # convert string config to dict
            response = requests.put(compute_url + vnf['node'] + '/' + vnf['name'], json=data)
            print('Adding VNF ' + vnf['name'] + ' at ' + vnf['node'] + '. Success: ' + str(response.status_code == requests.codes.ok))

        # connect instances along calculated edges
        for vlink in result['placement']['vlinks']:
            src = vlink['src_vnf']
            dst = vlink['dest_vnf']
            data = {'vnf_src_name': src, 'vnf_dst_name': dst, 'vnf_src_interface': 'output', 'vnf_dst_interface': 'input', 'bidirectional': 'True', 'weight': 'delay'}
            response = requests.put(network_url, json=data)
            print('Adding link from ' + src + ' to ' + dst + '. Success: ' + str(response.status_code == requests.codes.ok))
    #         vlink['emu_debug_info'] = response.text
    #
    # # dump updated result with emulation response info
    # with open(placement, 'w', newline='') as place_file:
    #     yaml.dump(result, place_file, default_flow_style=False)


def parse_args():
    parser = argparse.ArgumentParser(description='Triggers placement and then emulation')
    parser.add_argument('-a', '--algorithm', help='Placement algorithm ("bjointsp", "random", "greedy")', required=True, dest='alg')
    parser.add_argument('--network', help='Network input file (.graphml)', required=True, dest='network')
    parser.add_argument('--service', help='Service input file (.yaml)', required=True, dest='service',nargs='+')
    parser.add_argument('--sources', help='Sources input file (.yaml)', required=True, dest='sources')
    parser.add_argument(
        '--placeOnly',
        help='Only perform placement, do not trigger emulation.',
        required=False,
        default=False,
        action='store_true',
        dest='placeOnly')
    return parser.parse_args()


def main():
    args = parse_args()
    placements=[]
    if args.alg == 'bjointsp':
        print('\nStarting placement with B-JointSP (heuristic)\n')
        for service in args.service:
            placement = bjointsp.place(args.network, service, args.sources, cpu=1, mem=10, dr=50)
            placements.append(placement)
            write_placement2(args.network, args.service, args.sources, placements, 'bjointsp')
    elif args.alg == 'random':
        print('\nStarting random placement\n')
        for service in args.service:
            placement = random_placement.place(args.network, service, args.sources)
            placements.append(placement)
            write_placement2(args.network, args.service, args.sources, placements, 'random')
    elif args.alg == 'random2':
        print('\nStarting random2 placement\n')
        for service in args.service:
            placement = random_placement2.place(args.network, service, args.sources)
            placements.append(placement)

    elif args.alg == 'greedy':
        print('\nStarting greedy placement\n')
        for service in args.service:
            placement = greedy_placement.place(args.network, service, args.sources)
            placements.append(placement)
    else:
        raise ValueError('Unknown placement algorithm: {}. Use "bjointsp", "random", or "greedy"'.format(args.alg))

    if args.placeOnly:
        print('\nPlacement complete; no emulation (--placeOnly).')
    else:
        print('\n\nEmulating calculated placement:\n')
        emulate_placement(placement)


if __name__ == '__main__':
    main()