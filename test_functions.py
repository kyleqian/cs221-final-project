
import nltk
# def getCombinations(assignments, indicesUsed, currIndex):
# 		if currIndex == len(assignments) - 1:
# 			words = []
# 			print indicesUsed
# 			for i in range(len(indicesUsed)):
# 				index = indicesUsed[i]
# 				words.append(assignments[i][index])
# 			return [words]

# 		combinations = []
# 		assignment = assignments[currIndex]
# 		for i in range(len(assignments)):
# 			assignment = assignments[i]
# 			l = len(assignment)
# 			for j in range(l):
# 				indicesUsed[i] = j
# 				print "%s|%s" %(assignment, indicesUsed)
# 				combo = getCombinations(assignments, indicesUsed, currIndex + 1)
# 				combinations += combo
# 			indicesUsed[i] = 0

# 		return combinations

def getCombinations(assignments, result, elemIndex):
	if elemIndex == len(assignments):
		return [result]

	combinations = []
	currAssignment = assignments[elemIndex]
	for k in range(len(currAssignment)):
		rCopy = result[:] # deep copy
		rCopy.append(currAssignment[k])
		currCombinations = getCombinations(assignments, rCopy, elemIndex + 1)
		combinations += currCombinations
		#result.pop()
	return combinations

arr1 = ["a", "b","c"]
arr2 = ["d", "e"]
arr3 = ["f", "g"]

#assignments = [arr1, arr2]
assignments = [arr1, arr2, arr3]
combinations = getCombinations(assignments, [], 0)
print combinations
print len(combinations)

print nltk.help.upenn_tagset()
