from review_processor import stream_review

def test_review_processor(file_path):
    nuanced_review, process_review =  stream_review(file_path)
    print(nuanced_review, process_review)


if __name__ == "__main__":
    test_review_processor('data/PT24080015603/T09 – OOP – Classes/review_text.txt')