type MaybeId =
    { _tag: "Just", value: number }
    | { _tag: "Nothing", value: void };

const MaybeId = {
    Just: (value: number) => ({ _tag: "Just", value }),
    Nothing: (value: void) => ({ _tag: "Nothing", value })
};


function process_id(id: MaybeId): void {
    switch (id) {
        case MaybeId.Just(n):
            console.log("ID:", n);
            break;
        case MaybeId.Nothing(_):
            console.log("No ID provided");
            break;
    }
}

function main(): void {
    const a = MaybeId.Just(42);
    process_id(a);
    process_id(MaybeId.Nothing);
}

main();
