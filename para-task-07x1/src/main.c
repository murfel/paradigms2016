#include "thread_pool.h"
#include "computation.h"
#include <stdlib.h>
#include <stdio.h>

void comp1(void *args) {
    printf("comp1\n");
    thpool_complete_computation((struct Computation *)args);
}

void callback1(void *args) {
    printf("callback1\n");
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

    free(computation);
    thpool_finit(pool);
    free(pool);
}

int main() {
    test_simple();

    return 0;
}
