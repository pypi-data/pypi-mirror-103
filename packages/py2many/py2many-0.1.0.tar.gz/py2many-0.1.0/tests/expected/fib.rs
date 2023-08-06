fn fib(i: i32) -> i32 {
    if i == 0 || i == 1 {
        return 1;
    }
    return (fib((i - 1)) + fib((i - 2)));
}

fn main() {
    let rv: i32 = fib(5);
    println!("{}", rv);
}
