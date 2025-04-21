from flask import Flask, request, jsonify
import time, tracemalloc
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
import io
import contextlib
import ast
app = Flask(__name__)
CORS(app)

# Connect to MongoDB (local or Docker)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/analyzer")
mongo = PyMongo(app)


def estimate_complexity(code):
    # Parse the code into an Abstract Syntax Tree (AST)
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return "Unknown", "Unknown"

    # Initialize complexity estimates
    time_complexity = "O(1)"
    space_complexity = "O(1)"

    # Define a visitor class to analyze the AST
    class ComplexityVisitor(ast.NodeVisitor):
        def __init__(self):
            self.loops = 0
            self.recursions = 0
            self.data_structures = 0

        def visit_For(self, node):
            self.loops += 1
            self.generic_visit(node)

        def visit_While(self, node):
            self.loops += 1
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            # Check for recursive calls
            if any(isinstance(n, ast.Call) and n.func.id == node.name for n in ast.walk(node)):
                self.recursions += 1
            self.generic_visit(node)

        def visit_List(self, node):
            self.data_structures += 1
            self.generic_visit(node)

        def visit_Dict(self, node):
            self.data_structures += 1
            self.generic_visit(node)

        def visit_Set(self, node):
            self.data_structures += 1
            self.generic_visit(node)

        def visit_Tuple(self, node):
            self.data_structures += 1
            self.generic_visit(node)

    # Visit the AST nodes
    visitor = ComplexityVisitor()
    visitor.visit(tree)

    # Estimate time complexity
    if visitor.recursions > 0:
        time_complexity = f"O(n^{visitor.recursions})"  # r is the number of recursive calls
    elif visitor.loops > 0:
        time_complexity = f"O(n^{visitor.loops})"  # l is the number of nested loops

    # Estimate space complexity
    if visitor.data_structures > 0:
        space_complexity = "O(n)"  # Assuming linear space for data structures

    return time_complexity, space_complexity

@app.route('/analyze', methods=['POST'])
def analyze_code():
    try:
        data = request.get_json()
        code = data.get('code', '')

        # Start measuring
        tracemalloc.start()
        start_time = time.time()

        # Run the code (sandboxed in real apps!)
        # exec(code, {})
        
        # Capture the output of the code execution
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(code, {})
        print("Captured Output:", output.getvalue())

        time_taken = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Estimate complexity
        time_complexity, space_complexity = estimate_complexity(code)

        result = {
            "time_taken": time_taken,
            "peak_memory": peak,
            "output": output.getvalue(),
            "time_complexity": time_complexity,
            "space_complexity": space_complexity
        }

        # Save result to MongoDB
        mongo.db.reports.insert_one({
            "code": code,
            "time_taken": time_taken,
            "peak_memory": peak,
            "output": output.getvalue(),
            "time_complexity": time_complexity,
            "space_complexity": space_complexity,
            "timestamp": time.time()
        })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

