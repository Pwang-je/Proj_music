import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts);

Vue.component('apexchart', VueApexCharts);

var pie = new Vue({
    el: '#pie',
    components: {
        apexchart: VueApexCharts,
    },
    data: {
        series: [44, 55, 66, 77, 88],
        chartOptions: {
            labels: ['남성 솔로', '여성 솔로', '남성 그룹', '여성 그룹', '혼성 듀오'],
            responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        width: 200
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }]
        }
    }
});

