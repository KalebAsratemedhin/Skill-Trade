<template>
    <div class="p-5">
        <header class="text-center mb-5">
            <h1 class="text-3xl font-bold">Dashboard</h1>
        </header>
        <section class="flex flex-wrap gap-5 justify-center">
            <div 
                class="bg-white border border-gray-200 rounded-lg shadow-md p-5 w-72" 
                v-for="card in cards" 
                :key="card.id"
            >
                <h2 class="text-xl font-semibold mb-2">{{ card.title }}</h2>
                <p class="text-gray-600">{{ card.description }}</p>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: "Dashboard",
    data() {
        return {
            cards: [
                { id: 1, title: "Card 1", description: "This is the first card." },
                { id: 2, title: "Card 2", description: "This is the second card." },
                { id: 3, title: "Card 3", description: "This is the third card." },
            ],
        };
    },
};
</script>
