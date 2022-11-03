import hashlib as hl
from bitarray import bitarray
from os.path import exists

class BloomFilter:
	def __init__(self, num_bits:int, hash_functions:list ):
		# print("BloomFilter::init")
		self.bits = num_bits
		self.hash_functions = hash_functions
		self.ba = self.load_filter("files/rockyou.txt")
		# self.bitarray = bitarray(self.bits, endian="big")

	def load_filter(self, dict_file:str = None):
		print("BloomFilter::load_filter")
		file_name = f"bitarray_{len(self.hash_functions)}_{self.bits}.txt"
		# print(f"BloomFilter::load_filter file_name: {file_name}")
		if exists(file_name):
			bit_array = bitarray()
			with open(f"{file_name}", "rb") as f:
				bit_array.fromfile(f)
				# print(f"bit_array: {bit_array[:100]}")
			
			print(f"BloomFilter::load_filter - {file_name} loaded successfully")
		else:
			bit_array = bitarray(self.bits)
			
			for word in read_file(dict_file):
				for hf in self.hash_functions:
					bit = self._get_hash_index(hf, word)
					
					bit_array[bit] = 1
			
			with open(file_name, "wb") as f:
				bit_array.tofile(f)
		
		print("BloomFilter::load_filter complete")
		print(f"BloomFilter total values: {bit_array.count()} of {len(bit_array)}")
		ba_distro = list()
		print(f"BloomFilter Distrobution")
		for i in range(20):
			start = i * (len(bit_array) // 20)
			end = (i + 1) * (len(bit_array) // 20)
			print(f"{i}: {bit_array[start: end].count()} of {len(bit_array)}: {(bit_array[start: end].count()/ bit_array.count()):.4f}")

		return bit_array
	
	def _get_hash_index(self, hash_filter, word:bytes):
		
		working_hf = hash_filter.copy()
		working_hf.update(word)

		# shake_128 is a variable length digest, we need to pass length
		hf_digest = working_hf.digest(16) if "shake_" in working_hf.name else working_hf.digest()
		# print(f"hf_digest: {hf_digest}")

		return int.from_bytes(hf_digest, "big") % self.bits

	def test_filter(self, test_words:list, master_list:list):
		print("BloomFilter::test_filter")
		positive_words = list()
		negative_words = list()
		for word in test_words:
			results = bitarray(len(self.hash_functions))
			indices = list()
			for index, hf in zip(range(len(self.hash_functions)), self.hash_functions):
				hash_index = self._get_hash_index(hf, word)

				results[index] = self.ba[hash_index]
			
			if results.all():
				# print(f"{word} is in the list")
				positive_words.append(word)
			else:
				negative_words.append(word)
	
		print(f"positive_words: {len(positive_words)} negative_words: {len(negative_words)}")
		false_positives = set(positive_words) - set(master_list)
		false_negatives = set(negative_words).intersection(set(master_list))
		true_negatives = set(negative_words) - set(master_list)
		true_positives = set(positive_words).intersection(set(master_list))
		print(f"false positives: {len(false_positives)}")
		print(f"false negatives: {len(false_negatives)}")
		print(f"true positives: {len(true_positives)}")
		print(f"true negatives: {len(true_negatives)}")
		

def read_file(file_name:str) -> list:
	with open(file_name, "rb") as f:
		dictionary = f.read().split(b'\n')

	return dictionary

def hash_functions(num_functions:int = None):
	hash_functions = [
		hl.md5(), hl.sha3_224(), hl.blake2s(),
		hl.sha3_512(), hl.sha1(), hl.sha3_256(),
		hl.blake2b(), hl.shake_256(), hl.shake_128(),
		hl.sha256()
	]
	# hash_functions = [
	# 	hl.md5(), hl.sha3_224(), hl.blake2s(),
	# 	hl.sha3_512(), hl.sha1(), hl.sha3_256(),
	# 	hl.blake2b(), hl.new("sm3"), hl.shake_128(),
	# 	hl.sha256()
	# ]
	return hash_functions[:num_functions] if num_functions else hash_functions

"""
	The initial values were determined by the following website. Once I
	understood the math behind determining the values, I calculated them
	myself.

	The following methods are created using the following website: 
	https://hur.st/bloomfilter/

	These are calculated using the number of lines in rockyou.txt (14,344,392)
	and various desired false positive rates.

	k => number of hash algorithms. This is always an integer.
	m => number of bits in the bitarray
	n => number of inserted elements
	p => desired false positive rate, in decimal. e.g. 5% would be 0.05

	n => 14,344,392

	k = -log2(p)

	k = (m / n) * ln(2)

	(k / ln(2)) = (m / n)

	m = (k * n) / ln(2)
"""


def fp_five_percent():
	"""
		k = 4 (4.321928)
		m = 82,788,733 (89,440,499)
		n = 14,344,392
		p => 0.05
	"""
	print("fp_five_percent")
	# return (82_778_333, hash_functions(4))
	return (89_440_449, hash_functions(4))

def fp_one_percent():
	"""
		k = 7 (6.643856)
		m = 144,862,082 (137,491,831)
		n = 14,344,392
		p => 0.01
	"""	
	print("fp_one_percent")
	return (137_491_831, hash_functions(7))
	# return (144_862_082, hash_functions(6))
	# return (144_862_082, hash_functions(7))
	# return (159_348_269, hash_functions(7))

def fp_half_percent():
	"""
		k = 8 (7.643856)
		m = 165,556,665 (158,186,414)
		n = 14,344,392
		p => 0.005
	"""	
	print("fp_half_percent")
	# return (165_556_665, hash_functions(8))
	return (158_186_414, hash_functions(8))

def fp_tenth_percent():
	"""
		k = 10 (9.965784)
		m = 206,945,832 (206,237,746)
		n = 14,344,392
		p => 0.001
	"""	
	print("fp_tenth_percent")
	# return (206_945_832, hash_functions(10))
	return (206_237_746, hash_functions(10))

def main():
	filter_params = [fp_five_percent, fp_one_percent, fp_half_percent, fp_tenth_percent ]

	rockyou = read_file("files/rockyou.txt")
	test_words = read_file("files/dictionary.txt")
	# unique_words = set(test_words) - set(rockyou)

	print(f"bloom filter length: {len(rockyou)}")
	print(f"test_words length: {len(test_words)}")
	
	for param in filter_params:
		bf = BloomFilter(*param())
		bf.test_filter(test_words, rockyou)

if __name__ == "__main__":
	main()
