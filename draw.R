drawResult <- function(fname) {
    # http://stat.biopapyrus.net/graph/lines.html
    data <- read.table(fname)
    x <- 1:ncol(data)
    cols <- c('#0000ff', '#ff0000', '#ff00ff', # AVX
              '#0000a0', '#a00000', '#a000a0') # NoAVX
    plot(0, 0, type = "n", xlim = range(x), ylim = c(max(data), min(data)))
    for (i in 1:nrow(data)) {
        lines(x, data[i,], lwd = 2, col = cols[i])
    }
}