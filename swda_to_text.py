from swda import CorpusReader
from swda_utilities import *

# Processed data directory
data_dir = 'output_swda/'

# Corpus object for iterating over the whole corpus in .csv format
corpus = CorpusReader('swda_data/')

# If flag is set will only write utterances and not speaker or DA label
utterance_only_flag = False

# Excluded dialogue act tags i.e. x = Non-verbal
excluded_tags = ['x']
# Excluded characters for ignoring i.e. <laughter>
excluded_chars = {'<', '>', '(', ')', '-', '#'}

# Load training, test, validation and development splits
train_split = load_data(data_dir + 'train_split.txt')
test_split = load_data(data_dir + 'test_split.txt')
val_split = load_data(data_dir + 'eval_split.txt')
dev_split = load_data(data_dir + 'dev_split.txt')

# Files for all the utterances in the corpus and data splits
all_swda_file = "all_swda"
train_set_file = "train_set"
test_set_file = "test_set"
val_set_file = "eval_set"
dev_set_file = "dev_set"

# Remove old files if they exist, so we do not append to old data
remove_file(data_dir, all_swda_file, utterance_only_flag)
remove_file(data_dir, train_set_file, utterance_only_flag)
remove_file(data_dir, test_set_file, utterance_only_flag)
remove_file(data_dir, val_set_file, utterance_only_flag)
remove_file(data_dir, dev_set_file, utterance_only_flag)

# Process each transcript
for transcript in corpus.iter_transcripts(display_progress=False):

    # Process the utterances and create a dialogue object
    dialogue = process_transcript(transcript, excluded_tags, excluded_chars)

    # Append all utterances to all_swda_text_file
    append_dialogue_to_file(data_dir + all_swda_file, dialogue, utterance_only_flag)

    # Determine which set this dialogue belongs to (training, test or evaluation)
    set_dir = ''
    set_file = ''
    if dialogue.conversation_num in train_split:
        set_dir = data_dir + 'train/'
        set_file = train_set_file
    elif dialogue.conversation_num in test_split:
        set_dir = data_dir + 'test/'
        set_file = test_set_file
    elif dialogue.conversation_num in val_split:
        set_dir = data_dir + 'eval/'
        set_file = val_set_file

    # Create the directory if is doesn't exist yet
    if not os.path.exists(set_dir):
        os.makedirs(set_dir)

    # Write individual dialogue to train, test or validation folders
    write_dialogue_to_file(set_dir + dialogue.conversation_num, dialogue, utterance_only_flag)

    # Append all dialogue utterances to sets file
    append_dialogue_to_file(data_dir + set_file, dialogue, utterance_only_flag)

    # If it is also in the development set write it there too
    if dialogue.conversation_num in dev_split:

        set_dir = data_dir + 'dev/'
        set_file = dev_set_file

        # Create the directory if is doesn't exist yet
        if not os.path.exists(set_dir):
            os.makedirs(set_dir)

        # Write individual dialogue to dev folder
        write_dialogue_to_file(set_dir + dialogue.conversation_num, dialogue, utterance_only_flag)

        # Append all dialogue utterances to dev set file
        append_dialogue_to_file(data_dir + set_file, dialogue, utterance_only_flag)
