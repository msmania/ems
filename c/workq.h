class WorkQueue {
public:
    class Job {
    public:
        virtual ~Job() {}
        virtual void Run() = 0;
    };

private:
    enum WorkItemType {
        wiRun,
        wiExit,
        wiSync
    };

    class Event {
    private:
        pthread_mutex_t _lock;
        pthread_cond_t _cond;
        int _waitcount;
        int _maxcount;

    public:
        Event(int maxcount);
        virtual ~Event();
        void Wait();
    };

    class WorkItem {
    private:
        WorkItemType _type;
        void *_context;

    public:
        WorkItem(WorkItemType type, void *context);
        virtual ~WorkItem();
        virtual void Run();
    };

    int _numthreads;
    std::vector<pthread_t> _threads;
    Event _sync;
    pthread_mutex_t _taskqlock;
    std::queue<WorkItem*> _taskq;

    static void *StartWorkerthread(void *p);
    void *Workerthread(void *p);

public:
    WorkQueue(int numthreads);
    virtual ~WorkQueue();
    int CreateThreads();
    void JoinAll();
    void AddTask(Job *job);
    void Sync();
    void Exit();
};
