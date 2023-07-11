# Copyright (c) 2013-2014 Lingpeng Kong
# All Rights Reserved.
#
# This file is part of TweeboParser 1.0.
#
# TweeboParser 1.0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TweeboParser 1.0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with TweeboParser 1.0.  If not, see <http://www.gnu.org/licenses/>.



# This script reads from raw text tweets, one line per tweet and then run Twitter POS tagger on top of it. 
# (Tokenization and Converting to CoNLL format along the way.)

# Receive the arguments from the calling script. 


# Tagging using the pre-trained model -- this model remove the tweets we use as the test
ark-tweet-nlp-0.3.2/runTagger.sh --model pretrained_models/tagging_model --output-format conll $1 > $1_Tagger_output

python2 scripts/ConvertFromTaggingResToConll_1.py $1_Tagger_output > $1_tagger.out

#rm $1_Tagger_output
