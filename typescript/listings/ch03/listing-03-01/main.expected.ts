type Value =
    { _tag: "Num", value: number }
    | { _tag: "Text", value: number };

const Value = {
    Num: (value: number) => ({ _tag: "Num", value }),
    Text: (value: number) => ({ _tag: "Text", value })
};


function describe(value: Value): void {
    switch (value) {
        case Value.Num(n):
            console.log("It's a number:", n);
            break;
        case Value.Text(t):
            console.log("It's text:", t);
            break;
    }
}

function main(): void {
    describe(Value.Num(42));
    describe(Value.Text(99));
}

main();
