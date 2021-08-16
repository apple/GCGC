# datasets


All workloads generated here were made using the following Java application:

https://github.com/corretto/heapothesys/tree/master/HyperAlloc 


To generate these workloads, the following parameters were used.

    heapsize = 8G
    duration = 260 seconds
    gc-algorithm = 
        -XX:+UseParallelGC
        -XX:+UseG1GC
        -XX:+UseShenandoahGC
        -XX:+UseZGC
        -XX:+UseSerialGC


The command used was:

> java < gc-algorithm >  -Xmx8G -Xms8G -Xlog:gc*:./filename_log -jar HyperAlloc.jar -d 260
