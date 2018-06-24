package main

import (
	"fmt"
	"math"
	"os"
	"os/signal"
	"runtime"
)

type worker struct {
	stop chan struct{}
	res  chan int
}

func (w worker) doWork() {
	i := 0.0
	kNumber := 2350845.545
	for {
		select {
		case _ = <-w.stop:
			w.res <- int(i)
			close(w.res)
			return
		default:
			_ = math.Sqrt(kNumber * i)
			i++
		}
	}
}

func main() {
	s := make(chan os.Signal, 1)
	signal.Notify(s)

	ws := make([]worker, 0)
	for i := 0; i < runtime.NumCPU()/2; i++ {
		w := worker{
			stop: make(chan struct{}, 1),
			res:  make(chan int, 0),
		}

		go w.doWork()
		ws = append(ws, w)
	}

	_ = <-s
	for _, w := range ws {
		w.stop <- struct{}{}
	}

	count := 0
	for _, w := range ws {
		count += <-w.res
	}

	fmt.Printf("%v iterations\n", count)
}
