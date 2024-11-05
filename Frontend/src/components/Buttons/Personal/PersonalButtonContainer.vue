<template>
    <div class="button-container">
        <MySchedule/>
        <MyWFHRequests/>
        <MyWithdrawalRequests/>
    </div>
</template>

<style scoped>
.button-container {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 10px;
}
.button-container button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.button-container button:hover {
    background-color: #0056b3;
}
</style>