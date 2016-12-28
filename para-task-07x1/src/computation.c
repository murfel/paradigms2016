#include "thread_pool.h"
#include "computation.h"
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>

// Отправляет вычисление в очередь thread pool. Функция
// on_complete будет вызвана с параметром on_complete_arg,
// как только вычисление будет завершено функцией
// thpool_complete_computation. Также допустимо значение
// on_complete == NULL, в таком случае ничего дополнительно
// с on_complete делать не надо.
void thpool_submit_computation(
    struct ThreadPool *pool,
    struct Computation *computation,
    OnComputationComplete on_complete,
    void* on_complete_arg
) {
    computation->task.f = computation->f;
    computation->task.arg = computation->arg;
    computation->on_complete = on_complete;
    computation->on_complete_arg = on_complete_arg;

    pthread_mutex_init(&computation->guard, NULL);
    pthread_cond_init(&computation->finished_cond, NULL);
    computation->finished = false;

    thpool_submit(pool, &computation->task);
}

// Помечает вычисление как “завершённое с учётом подзадач” и
// вызывает функцию on_complete, которая была передана в
// thpool_submit_computation.
void thpool_complete_computation(struct Computation *computation) {
    pthread_mutex_lock(&computation->guard);
    computation->finished = true;
    pthread_cond_signal(&computation->finished_cond);
    pthread_mutex_unlock(&computation->guard);

    if (computation->on_complete) {
        (computation->on_complete)(computation->on_complete_arg);
    }
}

// Блокируется, пока вычислительная задача не завершена,
// освобождает выделенные в thpool_submit_computation ресурсы.
void thpool_wait_computation(struct Computation *computation) {
    pthread_mutex_lock(&computation->guard);
    while (!computation->finished) {
        pthread_cond_wait(&computation->finished_cond, &computation->guard);
    }
    pthread_mutex_unlock(&computation->guard);

    pthread_cond_destroy(&computation->finished_cond);
    pthread_mutex_destroy(&computation->guard);
}
