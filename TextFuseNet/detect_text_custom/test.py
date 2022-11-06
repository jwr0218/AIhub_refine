import pickle

with open('full_test_samples.pkl','rb') as fr:
    data = pickle.load(fr)
    print(data)

for i in data:
    name = i.split('\\')[3]
    print(name)