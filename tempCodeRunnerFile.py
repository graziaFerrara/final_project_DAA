N = ('Device 1', 'Device 2', 'Device 3', 'Device 4', 'Device 5')
# X = 7
# data = {'Device 1': (100, 99, 85, 77, 63), 'Device 2': (101, 88, 82, 75, 60), 'Device 3': (98, 89, 84, 76, 61), 'Device 4': (110, 65, 65, 67, 80), 'Device 5': (95, 80, 80, 63, 60)}
# partition = [['Device 1', 'Device 3', 'Device 5'], ['Device 2'], ['Device 4']]

# start = time()
# ds=DeviceSelection(N, X, data)
# C=ds.countDevices()
# subsets = [[] for i in range(C)]
# for i in range(C):
#     dev = ds.nextDevice(i)
#     while dev is not None:
#         subsets[i].append(dev)
#         dev = ds.nextDevice(i)
# end=time()-start

# if sorted(subsets) != sorted(partition):
#     print('FAIL')
# else:
#     print('True')
#     print(end)