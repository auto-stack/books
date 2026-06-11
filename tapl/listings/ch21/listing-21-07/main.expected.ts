// TypeScript
interface User {
    name: string;
    age: number;
}

const alice: User = { name: "Alice", age: 30 };
const json = JSON.stringify(alice);
console.log(json);

const parsed = JSON.parse(json);
console.log(parsed["name"]);
console.log(parsed["age"]);

const bob: User = { name: "Bob", age: 25 };
const users: User[] = [alice, bob];
const arrayJson = JSON.stringify(users);
console.log(arrayJson);
