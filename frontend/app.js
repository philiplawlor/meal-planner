class MealPlanner {
    constructor() {
        this.apiBaseUrl = 'http://localhost:3001';
        this.selectedMeal = null;
        this.mealPlans = [];
        this.filters = {
            cuisine: '',
            difficulty: '',
            dietary: ''
        };
        
        this.initialize();
    }

    async initialize() {
        await this.loadMeals();
        await this.loadFilters();
        
        // Set up event listeners
        document.getElementById('cuisineFilter').addEventListener('change', () => this.loadMeals());
        document.getElementById('difficultyFilter').addEventListener('change', () => this.loadMeals());
        document.getElementById('dietaryFilter').addEventListener('change', () => this.loadMeals());
    }

    async loadMeals() {
        try {
            console.log('Loading meals...');
            const response = await fetch('data.json');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Received data:', data);
            
            if (!data || !data.meals) {
                console.error('Invalid response format:', data);
                throw new Error('Invalid response format from server');
            }
            
            this.renderMeals(data.meals);
        } catch (error) {
            console.error('Error loading meals:', error);
            this.showError(`Failed to load meals: ${error.message}`);
        }
    }

    async loadFilters() {
        try {
            console.log('Loading filters...');
            const response = await fetch('data.json');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Received data:', data);
            
            if (!data || !data.meals) {
                console.error('Invalid response format:', data);
                throw new Error('Invalid response format from server');
            }
            
            // Get unique values for filters
            const meals = data.meals;
            const cuisines = Array.from(new Set(meals.map(meal => meal.cuisine)));
            const difficulties = Array.from(new Set(meals.map(meal => meal.difficulty)));
            const dietaryInfo = Array.from(new Set(
                meals.flatMap(meal => meal.dietary_info)
            ));

            this.populateFilters({
                cuisines,
                difficulties,
                dietary_info: dietaryInfo
            });
        } catch (error) {
            console.error('Error loading filters:', error);
            this.showError(`Failed to load filters: ${error.message}`);
        }
    }

    populateFilters(filters) {
        const cuisines = filters.cuisines;
        const difficulties = filters.difficulties;
        const dietaryInfo = filters.dietary_info;

        this.populateSelect('cuisineFilter', cuisines);
        this.populateSelect('difficultyFilter', difficulties);
        this.populateSelect('dietaryFilter', dietaryInfo);
    }

    populateSelect(selectId, items) {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">All</option>';
        items.forEach(item => {
            const option = document.createElement('option');
            option.value = item;
            option.textContent = item;
            select.appendChild(option);
        });
    }

    renderMeals(meals) {
        console.log('Rendering meals:', meals);
        
        if (!Array.isArray(meals) || meals.length === 0) {
            console.error('No meals to render:', meals);
            return;
        }

        // Get filter values
        const cuisineFilter = document.getElementById('cuisineFilter').value;
        const difficultyFilter = document.getElementById('difficultyFilter').value;
        const dietaryFilter = document.getElementById('dietaryFilter').value;

        // Filter meals
        const filteredMeals = meals.filter(meal => {
            const matchesCuisine = !cuisineFilter || meal.cuisine === cuisineFilter;
            const matchesDifficulty = !difficultyFilter || meal.difficulty === difficultyFilter;
            const matchesDietary = !dietaryFilter || meal.dietary_info.includes(dietaryFilter);
            
            return matchesCuisine && matchesDifficulty && matchesDietary;
        });

        console.log('Filtered meals:', filteredMeals);

        const container = document.getElementById('mealsContainer');
        if (!container) {
            console.error('Could not find meals container');
            return;
        }

        container.innerHTML = '';

        filteredMeals.forEach(meal => {
            if (!meal || !meal.name) {
                console.error('Invalid meal data:', meal);
                return;
            }

            const item = document.createElement('div');
            item.className = 'list-group-item meal-item';
            item.onclick = () => this.showMealDetails(meal);
            
            item.innerHTML = `
                <h6 class="mb-1">${meal.name}</h6>
                <p class="mb-1">${meal.description}</p>
                <div class="d-flex align-items-center">
                    <span class="difficulty-badge difficulty-${meal.difficulty}">
                        ${meal.difficulty}
                    </span>
                    <span class="ms-2">${meal.cuisine}</span>
                </div>
            `;

            container.appendChild(item);
        });
    }

    showMealDetails(meal) {
        const details = document.getElementById('mealDetails');
        details.classList.remove('d-none');
        
        document.getElementById('mealName').textContent = meal.name;
        document.getElementById('mealDescription').textContent = meal.description;
        
        const ingredientsList = document.getElementById('mealIngredients');
        ingredientsList.innerHTML = meal.ingredients.map(ing => 
            `<li>${ing.amount} ${ing.unit} ${ing.name}</li>`
        ).join('');

        const instructionsList = document.getElementById('mealInstructions');
        instructionsList.innerHTML = meal.instructions.map((step, index) => 
            `<li>${index + 1}. ${step}</li>`
        ).join('');

        this.selectedMeal = meal;
    }

    async createNewPlan() {
        const weekStart = new Date();
        weekStart.setDate(weekStart.getDate() - weekStart.getDay());

        const plan = {
            user_id: 'user123',
            week_start: weekStart.toISOString(),
            meals: []
        };

        try {
            const response = await fetch(`${this.apiBaseUrl}/meal-plans`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(plan)
            });

            const newPlan = await response.json();
            this.mealPlans.push(newPlan);
            this.renderMealPlans();
        } catch (error) {
            console.error('Error creating meal plan:', error);
            this.showError('Failed to create meal plan');
        }
    }

    async addMealToPlan() {
        if (!this.selectedMeal) return;

        const weekStart = new Date();
        weekStart.setDate(weekStart.getDate() - weekStart.getDay());

        const plan = {
            user_id: 'user123',
            week_start: weekStart.toISOString(),
            meals: [
                {
                    day: 1,
                    meal_type: 'breakfast',
                    meal_id: this.selectedMeal._id,
                    notes: ''
                }
            ]
        };

        try {
            const response = await fetch(`${this.apiBaseUrl}/meal-plans`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(plan)
            });

            const newPlan = await response.json();
            this.mealPlans.push(newPlan);
            this.renderMealPlans();
        } catch (error) {
            console.error('Error adding meal to plan:', error);
            this.showError('Failed to add meal to plan');
        }
    }

    showMealPlans() {
        document.getElementById('mealPlansContainer').classList.toggle('d-none');
        document.querySelector('.col-md-8').classList.toggle('col-md-12');
        document.querySelector('.col-md-4').classList.toggle('d-none');
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger';
        errorDiv.textContent = message;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(errorDiv, container.firstChild);
            setTimeout(() => errorDiv.remove(), 5000);
        }
    }
}

// Initialize the application
const app = new MealPlanner();
