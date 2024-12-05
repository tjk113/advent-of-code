import Text.Printf

count element list = length $ filter (== element) list

slideR text width offset = take width $ drop offset text

countHorizontal text = count "XMAS" windowed + count "SAMX" windowed
                       where windowed = [slideR text 4 n | n <- [0..length text]]

data Direction = Forwards | Backwards

verticalCount lines diag dir = count True
  [let column = [lines!!0!!(n+(offset!!0)),
                 lines!!1!!(n+(offset!!1)),
                 lines!!2!!(n+(offset!!2)),
                 lines!!3!!(n+(offset!!3))]
   in column == "XMAS" || column == "SAMX"
   | n <- [0..length (lines!!0) - (if diag then 4 else 1)]]
  where offset = if diag then case dir of
                   Forwards -> [0..3]
                   Backwards -> [3,2..0]
                 else replicate 4 0

countVertical text = sum
  [let shifted = slideR textLines 4 n in
   verticalCount shifted False Forwards
   + verticalCount shifted True Forwards
   + verticalCount shifted True Backwards
   | n <- [0..length textLines - 4]]
  where textLines = lines text

isMSRow (a:_:b:_) = (a == 'M' || a == 'S')
                    && (b == 'S' || b == 'M')
isMSRow _ = False

isARow (_:a:_) = a == 'A'
isARow _ = False

xCount lines = count True
  [let box = [slideR (lines!!0) 3 n,
              slideR (lines!!1) 3 n,
              slideR (lines!!2) 3 n]
   in isMSRow (box!!0)
   && isARow  (box!!1)
   && isMSRow (box!!2)
   && (box!!0)!!0 /= (box!!2)!!2
   && (box!!0)!!2 /= (box!!2)!!0
   | n <- [0..length (lines!!0) - 2]]

countX text = sum [xCount $ slideR textLines 3 n
                   | n <- [0..length textLines - 3]]
              where textLines = lines text

main :: IO ()
main = do
  text <- readFile "input.txt"
  printf "Part 1: %d\n" (countHorizontal text + countVertical text)
  printf "Part 2: %d\n" (countX text)
