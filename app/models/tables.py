import os
import string
from app import db
from app.controllers.env_configs import EnvConf


class LabelFile(db.Model):
    __tablename__ = "label_files"

    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(32), unique=False)
    name = db.Column(db.String(80), unique=False)
    positive_labels = db.Column(db.Integer, primary_key=False)
    negative_labels = db.Column(db.Integer, primary_key=False)

    def num_labels(self):
        return self.positive_labels+self.negative_labels

    def __init__(self, file_hash, name, positive_labels, negative_labels):
        self.file_hash = file_hash
        self.name = name
        self.positive_labels = positive_labels
        self.negative_labels = negative_labels

    def __repr__(self):
        return f'<LabelFile {self.id}:{self.file_hash}>'

class DatasetFile(db.Model):
    __tablename__ = "dataset_files"

    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(32), unique=False)
    name = db.Column(db.String(80), unique=False)
    words = db.Column(db.Integer, primary_key=False)

    def __init__(self, file_hash, name, words):
        self.file_hash = file_hash
        self.name = name
        self.words = words

    def __repr__(self):
        return f'<DatasetFile {self.id}:{self.file_hash}>'

    def get_text_data(self):
        folder = EnvConf.dataset_dir
        path = os.path.abspath(folder)+'/'+self.file_hash
        
        #string cleaning for training
        transtable = str.maketrans('', '', string.punctuation)
        with open(path) as f:
            lines = f.readlines()
        text_docs = []
        for line in lines:
            doc = line.translate(transtable).lower()
            doc_list = doc.split()
            text_docs.append(doc_list)
        return text_docs

class Word2VecModel(db.Model):
    __tablename__ = "w2v_models"

    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(36), unique=False)
    description = db.Column(db.Text, unique=False)
    words = db.Column(db.Integer, primary_key=False)
    min_count = db.Column(db.Integer, primary_key=False)
    window = db.Column(db.Integer, primary_key=False)
    iterations = db.Column(db.Integer, primary_key=False)
    
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset_files.id'))
    dataset = db.relationship('DatasetFile',foreign_keys=dataset_id)

    label_id = db.Column(db.Integer, db.ForeignKey('label_files.id'))
    label = db.relationship('LabelFile',foreign_keys=label_id)

    def __init__(self, file_hash, description, dataset_id, label_id):
        self.file_hash = file_hash
        self.description = description
        self.dataset_id = dataset_id
        self.label_id = label_id

    def __repr__(self):
        return f'<Word2VecModel {self.id}:{self.file_hash}>'