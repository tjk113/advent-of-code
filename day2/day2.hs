import Text.Printf 

isSafeStep cur next = let diff = abs $ cur - next
                      in diff >= 1 && diff <= 3

hasOrder op report = foldl (&&) True [(op) (report !! x) (report !! (x + 1)) | x <- [0..(length report - 2)]]

isOrdered report = hasOrder (>) report || hasOrder (<) report

isSafe report = foldl (&&) True [isSafeStep (report !! x) (report !! (x + 1)) | x <- [0..(length report - 2)]]
                && isOrdered report

isSafeTolerant report = isSafe report
                        || foldl (||) False [isSafe (remove report x) | x <- [0..(length report - 1)]]

remove xs index = [xs !! x | x <- [0..(length xs - 1)], x /= index]

count element list = length $ filter (== element) list

main :: IO ()
main = do
  lines <- lines <$> readFile "input.txt"
  let reports = [(map read $ words line) :: [Int] | line <- lines]
  printf "Part 1: %d\n" (count True $ map isSafe reports)
  printf "Part 2: %d\n" (count True $ map isSafeTolerant reports)
