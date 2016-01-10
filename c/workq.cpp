#include <pthread.h>
#include <unistd.h>
#include <vector>
#include <queue>
#include "workq.h"

#ifdef _LOG
#include <stdio.h>
#define LOGINFO printf
#else
#pragma GCC diagnostic ignored "-Wunused-value"
#define LOGINFO
#endif

WorkQueue::Event::Event(int maxcount) : _waitcount(0), _maxcount(maxcount) {
    pthread_mutex_init(&_lock, nullptr);
    pthread_cond_init(&_cond, nullptr);
}

WorkQueue::Event::~Event() {
    pthread_cond_destroy(&_cond);
    pthread_mutex_destroy(&_lock);
}

// Test Command: for i in {1..1000}; do ./t; done
void WorkQueue::Event::Wait() {
    LOGINFO("[%lx] start:wait\n", pthread_self());
    pthread_mutex_lock(&_lock);
    if (__sync_bool_compare_and_swap(&_waitcount, _maxcount, 0)) {
        pthread_cond_broadcast(&_cond);
    }
    else {
        __sync_fetch_and_add(&_waitcount, 1);
        pthread_cond_wait(&_cond, &_lock);
    }
    pthread_mutex_unlock(&_lock);
}

WorkQueue::WorkItem::WorkItem(WorkItemType type, void *context)
    : _type(type), _context(context) {}

WorkQueue::WorkItem::~WorkItem() {}

void WorkQueue::WorkItem::Run() {
    switch (_type) {
    case wiExit:
        LOGINFO("[%lx] exiting\n", pthread_self());
        pthread_exit(nullptr);
        break;
    case wiSync:
        if (_context) {
            ((Event*)_context)->Wait();
        }
        break;
    case wiRun:
        ((Job*)_context)->Run();
        break;
    default:
        break;
    }
}

void *WorkQueue::StartWorkerthread(void *p) {
    void *ret = nullptr;
    if (p) {
        ret = ((WorkQueue*)p)->Workerthread(p);
    }
    return ret;
}

void *WorkQueue::Workerthread(void *p) {
    while (true) {
        WorkItem *task = nullptr;
        pthread_mutex_lock(&_taskqlock);
        if (!_taskq.empty()) {
            task = _taskq.front();
            _taskq.pop();
        }
        pthread_mutex_unlock(&_taskqlock);
        if (task != nullptr) {
            task->Run();
            delete task;
        }
        else {
            usleep(10000);
        }
    }
}

WorkQueue::WorkQueue(int numthreads) : _numthreads(numthreads), _sync(numthreads) {
    pthread_mutex_init(&_taskqlock, nullptr);
    _threads.reserve(numthreads);
}

WorkQueue::~WorkQueue() {
    if (_threads.size() > 0) {
        JoinAll();
    }
    pthread_mutex_destroy(&_taskqlock);
}

int WorkQueue::CreateThreads() {
    int ret = 0;
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);
    for (int i = 0; i<_numthreads ; ++i) {
        pthread_t p = 0;
        ret = pthread_create(&p, &attr, StartWorkerthread, this);
        if (ret == 0) {
            _threads.push_back(p);
        }
        else {
            LOGINFO("pthread_create failed - %08x\n", ret);
            break;
        }
    }
    pthread_attr_destroy(&attr);
    return ret;
}

void WorkQueue::JoinAll() {
    for (auto &t : _threads) {
        pthread_join(t, nullptr);
    }
    _threads.clear();
}

void WorkQueue::AddTask(Job *job) {
    pthread_mutex_lock(&_taskqlock);
    _taskq.push(new WorkItem(wiRun, job));
    pthread_mutex_unlock(&_taskqlock);
}

void WorkQueue::Sync() {
    pthread_mutex_lock(&_taskqlock);
    for (int i = 0 ; i<_numthreads; ++i) {
        _taskq.push(new WorkItem(wiSync, &_sync));
    }
    pthread_mutex_unlock(&_taskqlock);
    _sync.Wait();
}

void WorkQueue::Exit() {
    pthread_mutex_lock(&_taskqlock);
    for (int i = 0 ; i<_numthreads; ++i) {
        _taskq.push(new WorkItem(wiExit, nullptr));
    }
    pthread_mutex_unlock(&_taskqlock);
}