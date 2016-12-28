#include <thread_pool.h>
#include <computation.h>
#include <stdlib.h>
#include <stdio.h>

void comp1(void *args) {
    printf("comp1\n");
    thpool_complete_computation((struct Computation *)args);
}

void callback1(void *args) {
    printf("callback1\n");
}

void comp2(void *args) {
    printf("comp2\n");
}

void callback2(void *args) {
    printf("callback2\n");
}

void comp3(void *args) {
    printf("comp3\n");
}

void callback3(void *args) {
    printf("callback3\n");
}


void test_simple() {
    struct ThreadPool *pool = malloc(sizeof(struct ThreadPool));
    thpool_init(pool, 2);

    struct Computation *computation = malloc(sizeof(struct Computation));

    computation->f = comp1;
    void * arg = (void *)computation;
    computation->arg = arg;

    thpool_submit_computation(
        pool,
        computation,
        callback1,
        NULL
    );

    thpool_wait_computation(computation);
}

void test_chain() {
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
}


int main() {
    test_simple();

    return 0;
}
