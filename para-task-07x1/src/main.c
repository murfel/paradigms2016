#include <thread_pool.h>
#include <computation.h>
#include <stdlib.h>
#include <stdio.h>

void comp1(void *args) {
    printf("comp1\n");
}

void callback1(void *args) {
    printf("callback1\n");
}

int main() {

    struct ThreadPool *pool = malloc(sizeof(struct ThreadPool));
    unsigned threads_nm = 2;
    thpool_init(pool, threads_nm);

    struct Computation *computation = malloc(sizeof(struct Computation));

    computation->f = comp1;
    void * arg = malloc(sizeof(int));
    computation->arg = arg;

    OnComputationComplete on_complete = callback1;
    void* on_complete_arg = malloc(sizeof(int));

    thpool_submit_computation(
        pool,
        computation,
        on_complete,
        on_complete_arg
    );

    thpool_wait_computation(computation);
    thpool_complete_computation(computation);

    return 0;
}
