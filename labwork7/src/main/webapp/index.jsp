<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%
    int[][] puzzle = (int[][]) request.getAttribute("puzzle");
    if (puzzle == null) {
        puzzle = new int[9][9];
    }
%>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cloud Sudoku</title>
    <style>
        body { background-color: #f0f2f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        h1 { color: #1a73e8; margin-bottom: 20px; }
        .game-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        table { border: 2px solid #333; border-collapse: collapse; margin: 0 auto; }
        td { width: 40px; height: 40px; border: 1px solid #ccc; padding: 0; }
        td:nth-child(3n) { border-right: 2px solid #333; }
        tr:nth-child(3n) td { border-bottom: 2px solid #333; }
        td:last-child { border-right: 2px solid #333; }
        tr:last-child td { border-bottom: 2px solid #333; }
        input { width: 100%; height: 100%; text-align: center; font-size: 18px; border: none; outline: none; color: #333; }
        .fixed { background-color: #e8f0fe; font-weight: bold; color: #1967d2; }
        .controls { margin-top: 20px; text-align: center; }
        button { background-color: #1a73e8; color: white; border: none; padding: 10px 24px; font-size: 16px; border-radius: 4px; cursor: pointer; transition: background 0.3s; }
        button:hover { background-color: #1557b0; }
    </style>
</head>
<body>
    <h1>Sudoku Lab 7</h1>
    <div class="game-container">
        <table>
            <tbody>
            <% for(int i=0; i<9; i++) { %>
                <tr>
                <% for(int j=0; j<9; j++) { 
                     int val = puzzle[i][j];
                     boolean isFixed = (val != 0);
                %>
                    <td>
                        <input type="number" min="1" max="9" 
                               value="<%= isFixed ? val : "" %>" 
                               class="<%= isFixed ? "fixed" : "" %>" 
                               <%= isFixed ? "readonly" : "" %> />
                    </td>
                <% } %>
                </tr>
            <% } %>
            </tbody>
        </table>
        <div class="controls">
            <button onclick="validateBoard()">Validate</button>
        </div>
    </div>
    <script>
        function validateBoard() {
            alert("Validation logic would go here. The initial board state was rendered by the Java Servlet.");
        }
    </script>
</body>
</html>