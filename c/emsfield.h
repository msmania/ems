typedef std::valarray<double> darray;

class Field {
private:
    class Force : public WorkQueue::Job {
    protected:
        Field *_field;
    public:
        Force(Field *field);
        virtual ~Force();
        virtual void load() = 0;
        virtual void Run() { load(); }
    };

    class Spring : public Force {
    private:
        int _n1;
        int _n2;
        double _k;
        double _l;
    public:
        Spring(Field *field, int n1, int n2, double k, double l);
        void load();
    };

    int _dim;
    darray _m;
    darray _friction;
    darray _accel;
    darray _velocity;
    darray _position;
    std::vector<Force*> _forces;
    WorkQueue *_workq;
    pthread_mutex_t _lock;
    std::vector<WorkQueue::Job*> _movetasks;

public:
    Field(int dim, int n);
    ~Field();
    void SetXY(int index, double x, double y);
    void BulkInit(int seed, double m, double friction, int fieldSize);
    void BulkInit(double m, double friction, const darray &position);
    void AddSpring(int n1, int n2, double k, double l);
    void MoveOneDim(double dt, int dim);
    void Move(double dt);
    const darray &Positions() const;
    double Energy() const;
    void Dump();
    void lock();
    void unlock();
};