import Text.Printf 
import Data.List
import Data.List.Split
import Data.Maybe

type Update = [Int]
type Rule = (Int, Int)

median :: [a] -> a
median list = list!!(length list `div` 2)

swap :: Int -> Int -> [a] -> [a]
swap a b l = (take a l)
          ++ (l!!b)
           : (drop (a+1) (take b l))
          ++ (l!!a)
           : (drop (b+1) l)

parseRule :: String -> Rule
parseRule rule = let (first:second:_) = read <$> splitOn "|" rule
                 in (first, second)

parseUpdate :: String -> Update
parseUpdate update = read <$> splitOn "," update

checkRule :: Update -> Rule -> Maybe Bool
checkRule update rule = if isJust first && isJust second then
                          Just (first < second)
                        else Nothing
                        where
                          first = elemIndex (fst rule) update
                          second = elemIndex (snd rule) update

isCorrect :: Update -> [Rule] -> Bool
isCorrect update rules = all id $ fromJust <$> filter isJust
                         [checkRule update rule | rule <- rules]

data UpdateKind = Correct | Incorrect

filterUpdates :: [Update] -> [Rule] -> UpdateKind -> [Update]
filterUpdates updates rules kind = [update | update <- updates,
                                    let check = isCorrect update rules
                                    in case kind of
                                      Correct -> check
                                      Incorrect -> not check]

_fixUpdate :: Update -> Rule -> Update
_fixUpdate update rule = if isJust check && (not $ fromJust check) then
                           swap indexB indexA update
                         else update
                         where
                           check = checkRule update rule
                           indexA = fromJust $ elemIndex (fst rule) update
                           indexB = fromJust $ elemIndex (snd rule) update

fixUpdate :: Update -> [Rule] -> [Rule] -> Update
fixUpdate update unappliedRules allRules
  | isCorrect update allRules = update
  | null unappliedRules = fixUpdate (_fixUpdate update (head allRules)) (tail allRules) allRules
  | otherwise = fixUpdate (_fixUpdate update (head unappliedRules)) (tail unappliedRules) allRules

fixUpdates :: [Update] -> [Rule] -> [Update]
fixUpdates updates rules = [fixUpdate update rules rules | update <- updates]


main :: IO ()
main = do
  text <- lines <$> readFile "input.txt"
  let split = splitWhen null text
  let orderingRules = parseRule <$> head split
  let updates = parseUpdate <$> (head $ tail split)
  let correctUpdates = filterUpdates updates orderingRules Correct
  let incorrectUpdates = filterUpdates updates orderingRules Incorrect
  let fixedUpdates = fixUpdates incorrectUpdates orderingRules
  printf "Part 1: %d\n" (sum $ median <$> correctUpdates)
  printf "Part 2: %d\n" (sum $ median <$> fixedUpdates)
