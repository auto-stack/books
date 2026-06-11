// TypeScript
let nums: number[] = [15, 3, 8, 1, 12, 7];

console.log("Before sort:");
console.log(nums.join(" "));

nums.sort((a, b) => a - b);

console.log("After sort:");
console.log(nums.join(" "));
