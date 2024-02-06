import argparse
import json
from tqdm import tqdm
parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',required=True)
parser.add_argument('-o','--output-file',required=True)

def main(args):
    
    coordinates_to_codes = {}

    print('Loading {}'.format(args.file))
    with open(args.file) as f:
        a = json.load(f)
        # Recursive routine to get at coordinates listed in element geometries
        def unpack_coordinates(output_array,input_array):
            # If current element is a list of lists, recurse
            if type(input_array[0]) is list:
                for i in input_array:
                    unpack_coordinates(output_array,i)
            # If routine is within a point list, add points to output array
            if type(input_array[0]) is float:
                key = str(input_array)
                output_array.append(key)

        print("Generating coordinate map..")
        for e in tqdm(a['features']):
            keys = []
            zip = e['properties']['ZCTA5CE10']
            unpack_coordinates(keys,e['geometry']['coordinates'])
            for k in keys:
                c = coordinates_to_codes.get(k,[])
                c.append(zip)
                coordinates_to_codes[k] = c

        print("Making zip_adjacency lists...")
        zip_adjacencies = {}
        for k in tqdm(coordinates_to_codes):
            for zip1 in coordinates_to_codes[k]:
                for zip2 in coordinates_to_codes[k]:
                    if zip1 != zip2:
                        a = zip_adjacencies.get(zip1,[])
                        if zip2 not in a:
                            a.append(zip2)
                            zip_adjacencies[zip1] = a

        print("Writing {}".format(args.output_file))
        with open(args.output_file,'w') as f:
            f.write(json.dumps(zip_adjacencies,indent=2))
                
if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
