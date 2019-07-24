const lookup = ([p, ...path], x) => (p === undefined) ? x : lookup(path, x)[p]

export default lookup
