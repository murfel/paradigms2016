#include <thread_pool.h>
#include <computation.h>
#include <stdlib.h>

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
    computation->task = malloc(sizeof(struct Task));
    computation->task->f = computation->f;
    computation->task->arg = computation->arg;
    computation->on_complete = on_complete;
    computation->on_complete_arg = on_complete_arg;

    thpool_submit(pool, computation->task);
}

// Помечает вычисление как “завершённое с учётом подзадач” и
// вызывает функцию on_complete, которая была передана в
// thpool_submit_computation.
void thpool_complete_computation(struct Computation *computation) {
    computation->task->finished = true;

    if (computation->on_complete) {
        (computation->on_complete)(computation->on_complete_arg);
    }
}

// Блокируется, пока вычислительная задача не завершена,
// освобождает выделенные в thpool_submit_computation ресурсы.
void thpool_wait_computation(struct Computation *computation) {
    thpool_wait(computation->task);
}
