#include <assert.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <../include/wsqueue.h>

#define SEED 42

struct PQSort_args {
    int l;
    int r;
    // ...
};

struct Task {
    void (*f)(void *); // функция, которую требуется выполнить
    void* arg; // данные, передаваемые функции в качестве параметра
    //<любые поля на усмотрение студента>

    pthread_cond_t cond;
    pthread_mutex_t guard;
};

struct ThreadPool {
    void * threads; // указатель на массив потоков
    struct wsqueue queue; // очередь тасков

    //<как-то хранящиеся потоки>
    //<как-то хранящиеся таски>
    //<любые поля на усмотрение студента>
};

void thpool_init(struct ThreadPool* pool, unsigned threads_nm);
void thpool_submit(struct ThreadPool* pool, struct Task* task);
void thpool_wait(struct Task* task);
void thpool_finit(struct ThreadPool* pool);

int data = 1234;

void* worker() {
    printf("Hello from thread! arg=%d\n", data);
    data += 10;
    return &data;
}

void fill_array_randomly(int * a, size_t size, int seed) {
    srand(seed);
    for (size_t i = 0; i < size; i++) {
        a[i] = rand();
    }
}

int compareMyType (const void * a, const void * b)
{
  if ( *(int*)a <  *(int*)b ) return -1;
  if ( *(int*)a == *(int*)b ) return 0;
  if ( *(int*)a >  *(int*)b ) return 1;
}

void swap(int * a, int * b) {
    int t = * a;
    * a = * b;
    * b = t;
}

void partition(int l, int r, int * a, int x, int * i, int * j) {  // [l, j](j, i)[i, r]
    *i = l;
    *j = r;
    while (*i <= *j) {
        while (a[*i] < x) { (*i)++; }
        while (a[*j] > x) { (*j)--; }
        if (*i <= *j) {
            swap(a + *i, a + *j);
            (*i)++;
            (*j)--;
        }
    }
}

void pqsort(int l, int r, int * a, int depth, int depth_limit) { // [l, r]
    if (depth > depth_limit) {
        qsort(a + l, r - l + 1, sizeof(int), compareMyType);
    }
    if (l >= r) { return; }
    int i, j;
    int x = a[rand() % (r - l) + l];
    partition(l, r, a, x, &i, &j);
    pqsort(l, j, a, depth + 1, depth_limit);
    pqsort(i, r, a, depth + 1, depth_limit);
}

void run_tests() {
    int a1 = 5;
    int b1 = 8;
    swap(&a1, &b1);
    assert(a1 == 8);
    assert(b1 == 5);

    int a[10];
    for (int i = 0; i < 10; i++) {
        a[i] = rand() % 10;
    }

    int i, j;
    int x = 6;
    partition(0, 9, a, x, &i, &j);

    int k;
    for (k = 0; k <= j; k++) {
        assert(a[k] <= x);
    }
    for (; k < i; k++) {
        assert(a[k] == x);
    }
    for (; k <= 9; k++) {
        assert(a[k] >= x);
    }

    pqsort(0, 9, a, 0, 1);

    for (int i = 1; i < 10; i++) {
        assert(a[i - 1] <= a[i]);
    }
}

void check_elem_order(int * a, int size) {
    for (int i = 1; i < size; i++) {
        assert(a[i - 1] <= a[i]);
    }
}

int main(int argc, char **argv) {

    size_t size = atoi(argv[2]);
    int * a = malloc(size * sizeof(int));
    fill_array_randomly(a, size, SEED);

    pqsort(0, size, a, 0, atoi(argv[3]));

    for (size_t i = 1; i < size; i++) {
        assert(a[i - 1] <= a[i]);
    }

    free(a);

/*
    pthread_t id;
    assert(pthread_create(&id, NULL, worker, NULL) == 0);
    pthread_detach(id);
    assert(pthread_join(id, NULL) == 0);
    printf("data is %d\n", data);
*/

    return 0;
}

/*

void merge_sort(int l, int r) {
if (l + 1 == r) return;
Thread t1(merge_sort, l, (l + r) / 2);
Thread t2(merge_sort, (l + r) / 2, r);
t1.start(); t2.start(); // Запускаем потоки.
t1.join(); t2.join(); // Ждём завершения.
merge(l, r);
}

*/
