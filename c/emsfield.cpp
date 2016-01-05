#include <stdio.h>
#include <random>
#include <valarray>
#include <vector>
#include "emsfield.h"

std::default_random_engine generator;
std::uniform_real_distribution<double> distribution(0.0, 1.0);

Field::Force::Force(Field *field) : _field(field) {}

Field::Force::~Force() {}

Field::Spring::Spring(Field *field, int n1, int n2, double k, double l)
    : Force(field), _n1(n1), _n2(n2), _k(k), _l(l) {
}

void Field::Spring::load() {
    std::valarray<double> diff(_field->_dim);
    int i, n = _field->_m.size();
    double norm = .0;
    for (i = 0 ; i < _field->_dim ; ++i) {
        diff[i] = _field->_position[_n2 + i * n] - _field->_position[_n1 + i * n];
        norm += diff[i] * diff[i];
    }
    norm = sqrt(norm);
    for (i = 0 ; i < _field->_dim ; ++i) {
        double f = _k * (1 - _l / norm) * diff[i];
        _field->_accel[_n1 + n * i] += f / _field->_m[_n1];
        _field->_accel[_n2 + n * i] += -f / _field->_m[_n2];
    }
}

Field::Field(int dim, int n)
    : _dim(dim),
      _m(n),
      _friction(n),
      _accel(dim * n),
      _velocity(dim * n),
      _position(dim * n)
{}

Field::~Field() {
    for (auto &f : _forces) {
        if (f != nullptr) {
            delete f;
        }
    }
}

void Field::SetXY(int index, double x, double y) {
    _position[index] = x;
    _position[index + _m.size()] = y;
}

void Field::BulkInit(int seed, double m, double friction, int fieldSize) {
    _m = m;
    _friction = friction;
    _velocity = .0;
    _accel = .0;
    generator.seed(seed);
    for (int i = 0 ; i < (int)_position.size() ; ++i) {
        _position[i] = (distribution(generator) * 2 - 1) * fieldSize;
    }
}

void Field::BulkInit(double m, double friction, const darray &position) {
    _m = m;
    _friction = friction;
    _velocity = .0;
    _accel = .0;
    _position = position;
}

void Field::AddSpring(int n1, int n2, double k, double l) {
    _forces.push_back(new Spring(this, n1, n2, k, l));
}

void Field::Move(double dt) {
    int i, j, n = _m.size();
    _accel = .0;
    for (auto &f : _forces) {
        if (f != nullptr) {
            f->load();
        }
    }
    for (i = 0 ; i < _dim ; ++i) {
        for (j = 0 ; j < n ; ++j) {
            int idx = j + i * n;
            _velocity[idx] += dt * _accel[idx];
            _velocity[idx] -= _velocity[idx] * _friction[j] / _m[j];
            _position[idx] += dt * _velocity[idx];
        }
    }
}

const darray &Field::Positions() const {
    return _position;
}

double Field::Energy() const {
    double e = .0;
    int n = _m.size();
    for (int i = 0 ; i < n ; ++i) {
        double vv = .0;
        for (int j = 0 ; j < _dim ; ++j) {
            vv += _velocity[i + j * n] * _velocity[i + j * n];
        }
        e += _m[i] * vv;
    }
    return e;
}

void Field::Dump() {
    int n = _m.size();
    for (int i = 0 ; i < (int)_m.size() ; ++i) {
        printf("[");
        for (int j = 0 ; j < _dim ; ++j) {
            printf("% 3.3f", _position[i + j * n]);
        }
        printf(" ]\n");
    }
}