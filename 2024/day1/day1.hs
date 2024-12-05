import Data.List
import Text.Printf

count element list = length $ filter (== element) list

main :: IO ()
main = do
  lines <- lines <$> readFile "input.txt"
  let pairs = [(read $ p !! 0, read $ p !! 1) | p <- words <$> lines]
  let xs = sort [fst p | p <- pairs]
  let ys = sort [snd p | p <- pairs]
  let len = length xs
  -- Because the lists are pre-sorted, `list !! n`
  -- returns the nth smallest element of `list`.
  printf "Part 1: %d\n" (sum [abs ((xs !! n) - (ys !! n)) | n <- [0..len-1]])
  printf "Part 2: %d\n" (sum [x * count x ys | x <- xs])
