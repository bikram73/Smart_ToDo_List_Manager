const calendarEl = document.getElementById('calendar');
const currentMonthEl = document.getElementById('currentMonth');
let currentDate = new Date();

function renderCalendar(tasks) {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    currentMonthEl.innerText = new Date(year, month).toLocaleString('default', { month: 'long', year: 'numeric' });
    
    // Use CSS Grid for 7 columns layout
    let html = '<div class="d-grid" style="grid-template-columns: repeat(7, 1fr); gap: 5px;">';
    
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    
    days.forEach(day => {
        html += `<div class="text-center fw-bold text-muted" style="font-size: 0.8rem; padding-bottom: 5px;">${day}</div>`;
    });

    // Empty slots
    for (let i = 0; i < firstDay; i++) {
        html += `<div></div>`;
    }

    const today = new Date();
    
    for (let day = 1; day <= daysInMonth; day++) {
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        
        // Check tasks for this date
        const dayTasks = tasks.filter(t => t.task_date === dateStr);
        const hasTasks = dayTasks.length > 0;
        const hasIncomplete = dayTasks.some(t => t.status !== 'completed');
        
        const isToday = day === today.getDate() && month === today.getMonth() && year === today.getFullYear();
        const isPast = new Date(dateStr) < new Date(today.toDateString());

        let indicator = '<div style="height: 6px;"></div>'; // Placeholder
        let cellClass = 'bg-light'; 
        let textClass = 'text-dark';

        if (isToday) {
            // Blue dot for today
            indicator = '<div class="rounded-circle bg-primary mx-auto" style="width: 6px; height: 6px;"></div>';
            cellClass = 'bg-white border border-primary';
        } else if (isPast && hasIncomplete) {
            // Red dot for past incomplete
            indicator = '<div class="rounded-circle bg-danger mx-auto" style="width: 6px; height: 6px;"></div>';
        } else if (hasTasks) {
            // Green dot for tasks exist
            indicator = '<div class="rounded-circle bg-success mx-auto" style="width: 6px; height: 6px;"></div>';
        }

        html += `
            <div class="text-center p-2 rounded ${cellClass}" 
                 onclick="filterTasksByDate('${dateStr}')" 
                 style="cursor: pointer; transition: 0.2s; min-height: 50px; display: flex; flex-direction: column; justify-content: center;">
                <span class="fw-bold small ${textClass}">${day}</span>
                <div class="mt-1">${indicator}</div>
            </div>
        `;
    }
    html += '</div>';

    // Add Legend
    html += `
        <div class="d-flex justify-content-center mt-3 gap-3 small text-muted">
            <div class="d-flex align-items-center"><div class="rounded-circle bg-success me-1" style="width: 8px; height: 8px;"></div> Tasks</div>
            <div class="d-flex align-items-center"><div class="rounded-circle bg-primary me-1" style="width: 8px; height: 8px;"></div> Today</div>
            <div class="d-flex align-items-center"><div class="rounded-circle bg-danger me-1" style="width: 8px; height: 8px;"></div> Overdue</div>
        </div>
    `;

    calendarEl.innerHTML = html;
}

function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    fetchTasks(); // Re-fetch to update calendar
}

function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    fetchTasks();
}

async function filterTasksByDate(dateStr) {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`/api/todos/date/${dateStr}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const tasks = await response.json();
        renderTasks(tasks);
        // Update header to show selected date
        const header = document.getElementById('tasksHeader');
        if(header) header.innerText = `Tasks for ${dateStr}`;
    } catch (error) {
        console.error(error);
    }
}