// TypeScript
interface Person {
    name: string;
    age: number;
}

let people: Person[] = [
    { name: "Zoe", age: 25 },
    { name: "Al", age: 60 },
    { name: "John", age: 1 },
];

console.log("Sorted by age:");
people.sort((a, b) => a.age - b.age);
for (const p of people) {
    console.log(`  ${p.name} (${p.age})`);
}
