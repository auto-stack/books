type Shape =
    { _tag: "Circle", value: number }
    | { _tag: "Square", value: number };

const Shape = {
    Circle: (value: number) => ({ _tag: "Circle", value }),
    Square: (value: number) => ({ _tag: "Square", value })
};


function area(shape: Shape): void {
    switch (shape) {
        case Shape.Circle(r):
            console.log("Circle area:", 3.14 * r * r);
            break;
        case Shape.Rectangle(w):
            console.log("Rectangle area:", w * w);
            break;
    }
}

function main(): void {
    const c = Shape.Circle(5);
    const s = Shape.Square(4);
    area(c);
    area(s);
}

main();
