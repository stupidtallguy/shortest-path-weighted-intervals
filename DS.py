from bisect import bisect_right
import sys


def _token_stream():
    """
    Robust token reader:
    - If input is piped/redirected: read all bytes fast.
    - If running interactively (tty): read lines until enough tokens exist.
    No prompts / no debug output.
    """
    if not sys.stdin.isatty():
        data = sys.stdin.buffer.read().split()
        for t in data:
            yield t
        return

    # Interactive: user types lines; stop only when enough tokens consumed by caller.
    # (User can paste the whole input; no prompts printed.)
    while True:
        line = sys.stdin.readline()
        if not line:  # EOF
            return
        for t in line.split():
            yield t.encode()  # keep same type as .split() on bytes


def solve():
    it = _token_stream()

    try:
        n = int(next(it))
    except StopIteration:
        return

    if n <= 0:
        return

    # Read intervals: (a, b, w, original_index)
    intervals = []
    for idx in range(n):
        try:
            a = int(next(it)); b = int(next(it)); w = int(next(it))
        except StopIteration:
            # Incomplete input; exit quietly (or you can raise an error).
            return
        intervals.append((a, b, w, idx))

    # Sort by right endpoint b (scan order)
    intervals.sort(key=lambda x: x[1])

    a = [t[0] for t in intervals]
    b = [t[1] for t in intervals]
    w = [t[2] for t in intervals]
    orig = [t[3] for t in intervals]  # sorted_index -> original input index

    # Succ(i) = smallest index l such that b[l] > a[i], else i
    succ = [0] * n
    for i in range(n):
        j = bisect_right(b, a[i])
        succ[i] = j if j < n else i

    # DSU
    parent = list(range(n))
    size = [1] * n

    # For each DSU root, store which interval index is the representative "parent interval"
    rep_parent = [-1] * n

    # Active-ness is tracked on DSU roots (interpretation follows your earlier design)
    is_active = [False] * n

    # Labels (distance)
    label = [-1] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> int:
        rx = find(x)
        ry = find(y)
        if rx == ry:
            return rx
        if size[ry] > size[rx]:
            rx, ry = ry, rx
        parent[ry] = rx
        size[rx] += size[ry]

        # Merge metadata
        if rep_parent[rx] == -1 and rep_parent[ry] != -1:
            rep_parent[rx] = rep_parent[ry]
        is_active[rx] = is_active[rx] or is_active[ry]
        return rx

    def set_root_rep(x: int, rep: int, active: bool):
        r = find(x)
        rep_parent[r] = rep
        is_active[r] = active
        return r

    # Stacks
    active_stack = []
    special_stack = []

    # Source interval = first in sorted-by-b order (same as your current approach)
    label[0] = w[0]
    set_root_rep(0, 0, True)
    active_stack.append(0)

    for i in range(1, n):
        j = succ[i]
        rj = find(j)

        if j == i:
            # Special inactive / loose component
            set_root_rep(i, rep_parent[rj], False)
            special_stack.append(i)
            continue

        if is_active[rj]:
            # Overlaps an active component: compute label from the representative parent
            pj = rep_parent[rj]
            if pj == -1:
                pj = j  # safe fallback
            label[i] = label[pj] + w[i]

            # Absorb all specials into i
            while special_stack:
                x = special_stack.pop()
                union(i, x)
                # Keep i as the rep of the merged set
                set_root_rep(i, i, True)

            # Ensure i's set is active and uses i as representative
            set_root_rep(i, i, True)

            # Pop actives that should be merged (monotonicity condition)
            while active_stack and label[i] < label[active_stack[-1]]:
                x = active_stack.pop()
                union(i, x)
                set_root_rep(i, i, True)

            active_stack.append(i)
        else:
            # Merge into special inactive component
            union(rj, i)
            set_root_rep(i, rep_parent[find(i)], False)
            special_stack.append(i)

    # Finalize labels for any unlabeled interval in a component with a known representative
    for i in range(n):
        if label[i] == -1:
            ri = find(i)
            pj = rep_parent[ri]
            if pj != -1 and label[pj] != -1:
                label[i] = label[pj] + w[i]

    # Output in original input order (1-based)
    ans_by_input = [0] * n
    for sorted_i in range(n):
        ans_by_input[orig[sorted_i]] = label[sorted_i]

    out_lines = []
    for k in range(n):
        out_lines.append(f"{k+1} {ans_by_input[k]}")
    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    solve()
