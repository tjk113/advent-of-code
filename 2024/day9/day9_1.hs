import Text.Printf 
import Data.Maybe
import Data.List

replaceFirst :: Eq a => a -> a -> [a] -> [a]
replaceFirst a b l = if isJust i then
                       take i' l ++ b : drop (i'+1) l
                     else l
                     where
                       i = elemIndex a l
                       i' = fromJust i

replaceLast :: Eq a => a -> a -> [a] -> [a]
replaceLast a b l = reverse $ replaceFirst a b (reverse l)

padToLengthWithMaybe :: Int -> [a] -> [Maybe a]
padToLengthWithMaybe len list = [if i < length list then Just (list!!i) else Nothing
                                 | i <- [0..len - 1]]

intertwine' :: [a] -> [a] -> [a]
intertwine' (a:as) (b:bs) = a : b : intertwine' (as) (bs)
intertwine' [] [] = []

intertwine :: [a] -> [a] -> [a]
intertwine from into = fromJust <$> filter isJust (intertwine' into' from')
                       where
                         toMaybeWithPad = \a b -> if length a > length b then
                                                    padToLengthWithMaybe (length a) b
                                                  else Just <$> b
                         from' = toMaybeWithPad into from
                         into' = toMaybeWithPad from into

expandBlocks :: [(Int, Int)] -> [[Int]]
expandBlocks blocks = map (\(idNum, size) -> replicate size idNum) blocks

isFree :: [Int] -> Bool
isFree block = -1 `elem` block

isCompressedPart1 :: [[Int]] -> Bool
isCompressedPart1 blocks = numFreeBlocks == (length $ filter isFree (drop ((length blocks) - numFreeBlocks) blocks))
                           where
                             numFreeBlocks = (sum $ map length $ filter isFree blocks)

compressPart1 :: [[Int]] -> [[Int]]
compressPart1 blocks = until isCompressedPart1
  (\curBlocks ->
    let curFree = head (filter isFree curBlocks)
        curFile = last curBlocks in
        if (not . null) curFile then
          replaceFirst curFree (replaceFirst (-1) (head curFile) curFree)
            $ replaceLast curFile (init curFile) curBlocks
        else filter (not . null) curBlocks)
  blocks

checksum :: [Int] -> Int
checksum blocks = sum $ map (\a -> fst a * snd a) $ filter (\a -> snd a /= -1) (zip [0..] blocks)

main :: IO ()
main = do
  text <- readFile "input.txt"
  let diskMap = map read (map (\c -> [c]) text) :: [Int]
      fileBlocks = map (\a -> (fst a, snd $ snd a))
              $ zip [0..] (filter (\a -> even $ fst a) (zip [0..] diskMap))
      freeBlocks = map (\a -> (-1, snd a))
                   $ filter (\a -> odd $ fst a) (zip [0..] diskMap)
      blocks = expandBlocks $ intertwine freeBlocks fileBlocks
      compressedPart1 = compressPart1 blocks
  -- mapM_ putStr $ map (\c -> if c == "-1" then "." else c) $ map show $ compressedPart1
  printf "Part 1: %d\n" (checksum $ concat compressedPart1)