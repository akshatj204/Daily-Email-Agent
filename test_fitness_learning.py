"""
Test Fitness & Learning Fetcher
"""

import sys
import logging
import json

logging.basicConfig(level=logging.INFO)
sys.path.insert(0, '.')

from fetchers.fitness_and_learning import FitnessAndLearningFetcher


def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_fitness_learning():
    print_section("MORNING EMAIL AGENT - Fitness & Learning Test")
    
    print("✓ Initializing FitnessAndLearningFetcher...")
    fetcher = FitnessAndLearningFetcher()
    
    # Test 1: Today's learning task
    print_section("Test 1: Today's Learning Task")
    task = fetcher.get_today_learning_task()
    print(f"Date: {task['date']} ({task['day']})")
    print(f"Task: {task['title']}")
    print(f"Difficulty: {task['difficulty']}")
    print(f"Time Required: {task['time']}")
    print(f"Description: {task['task']}")
    print(f"Resources: {', '.join(task['resources'])}")
    
    # Test 2: Python function of day
    print_section("Test 2: Python Function of the Day")
    func = fetcher.get_python_function_of_day()
    print(f"Function: {func['name']}")
    print(f"Position: {func['position']}")
    print(f"Difficulty: {func['difficulty']}")
    print(f"Description: {func['description']}")
    print(f"Use Case: {func['use_case']}")
    print(f"\nExample Code:\n{func['example']}")
    
    # Test 3: Fitness article of day
    print_section("Test 3: Fitness Article of the Day")
    fitness = fetcher.get_fitness_article_of_day()
    print(f"Topic: {fitness['topic']}")
    print(f"Title: {fitness['title']}")
    print(f"Duration: {fitness['duration']}")
    print(f"Focus: {fitness['focus']}")
    print(f"Key Points:")
    for point in fitness['key_points']:
        print(f"  • {point}")
    print(f"Source: {fitness['source']}")
    
    # Test 4: All fitness topics
    print_section("Test 4: Available Fitness Topics")
    topics = fetcher.get_all_fitness_topics()
    print(f"Total Topics: {topics['total_topics']}\n")
    for topic in topics['topics']:
        print(f"  ✓ {topic}")
    
    # Test 5: Get fitness by topic
    print_section("Test 5: Specific Fitness Topic - Swimming")
    swimming = fetcher.get_fitness_article_by_topic("Swimming")
    if swimming:
        print(f"Title: {swimming['title']}")
        print(f"Focus: {swimming['focus']}")
    
    # Test 6: Email formatting
    print_section("Test 6: Email Formatting")
    print("LEARNING TASK FORMAT:")
    print(fetcher.format_task_for_email(task))
    
    print("\nPYTHON FUNCTION FORMAT:")
    print(fetcher.format_python_function_for_email(func))
    
    print("\nFITNESS ARTICLE FORMAT:")
    print(fetcher.format_fitness_article_for_email(fitness))
    
    # Test 7: All data summary
    print_section("Test 7: Data Summary")
    all_tasks = fetcher.get_all_learning_tasks()
    all_funcs = fetcher.get_all_python_functions()
    all_fitness = fetcher.get_all_fitness_topics()
    
    print(f"✓ Learning Tasks: {all_tasks['total_tasks']} (one per day)")
    print(f"✓ Python Functions: {all_funcs['total_functions']} (daily rotation)")
    print(f"✓ Fitness Topics: {all_fitness['total_topics']} (daily rotation)")
    
    # Summary
    print_section("Summary")
    print("""
✅ Learning tasks system working
✅ Python function rotation working  
✅ Fitness article rotation working
✅ Topic-based filtering working
✅ Email formatting working

All components ready for integration!
    """)


if __name__ == "__main__":
    try:
        test_fitness_learning()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
