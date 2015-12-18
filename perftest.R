TestAll <- function(size, iter) {
    tester <- function(iter, v1, v2) {
        for (i in 1:iter) {
            d = runif(1) * 4 - 2
            v1 = v1 + d * v2
        }
    }
    print('*** matrix(n, 2) ***')
    v1 <- matrix(runif(size * 2), ncol=2)
    v2 <- matrix(runif(size * 2), ncol=2)
    result <- system.time(tester(iter, v1, v2))
    print(paste('time =', result['elapsed'], '(s)'), quote=F)
}