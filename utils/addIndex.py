with open('../data/dantri.jl') as f:
    count = 0
    with open('data.json',mode='w') as f1:
        for line in f:
            f1.write('{"index":{"_index":"dantri","_id":'+str(count)+'}}')
            f1.write('\n')
            f1.write(line)
            count += 1
    f1.close
f.close

