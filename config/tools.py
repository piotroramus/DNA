class Tool(object):
  def __init__(self, name, module_path):
    self.name = name
    self.module_path = module_path

ngs_tools = [ Tool('bwa', 'bwa'),
          Tool('Java', 'apps/java'),
          Tool('Picard', 'apps/picard/1.140'),
          Tool('GATK', 'tools/gatk'),
          Tool('SamTools', 'tools/samtools/0.1.19') ]


def dictify(tools):
	dictionary = {}
	for tool in tools:
		dictionary[tool.name] = tool.module_path
	return dictionary


ngs_tools_dict = dictify(ngs_tools)