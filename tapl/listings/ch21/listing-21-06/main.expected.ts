// TypeScript

interface User {
    name: string;
    age: number;
    email: string;
}

function main(): void {
    const alice: User = { name: "Alice", age: 30, email: "alice@example.com" };
    const json: string = JSON.stringify(alice);
    console.log(json);

    const parsed: User = JSON.parse(json) as User;
    console.log(parsed.name);
    console.log(parsed.age);

    const pretty: string = JSON.stringify(alice, null, 2);
    console.log(pretty);

    const bob: User = { name: "Bob", age: 25, email: "bob@example.com" };
    const users: User[] = [alice, bob];
    const usersJson: string = JSON.stringify(users);
    console.log(usersJson);
}

main();
