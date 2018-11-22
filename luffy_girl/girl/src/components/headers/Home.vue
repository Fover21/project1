<!--轮播图片控制-->
<template id="homeimg">
    <el-carousel indicator-position="outside" height="480px">
        <!--循环展出图片-->
        <el-carousel-item v-for="item in homePageImgArray" :key="item">
            <img :src="item.sources" class="banner_img"/>
        </el-carousel-item>
    </el-carousel>
</template>

<script>
    // 如果需要动态绑定属性，必须加上冒号，否则属性后面的值会被当成固定的
    //  首页轮播页面

    export default {
        name: "Home",
        data() {
            return {
                homePageImgArray: [
                    {
                        sources: 'https://hcdn1.luffycity.com/static/frontend/index/banner1(4)_1539945492.0492468.png',
                        id: 1
                    },
                    {
                        sources: 'https://hcdn1.luffycity.com/static/frontend/index/%E9%AA%91%E5%A3%AB(1)_1539945488.713867.png',
                        id: 2
                    },
                    {
                        sources: 'https://hcdn1.luffycity.com/static/frontend/index/banner%203_1538021864.9051478.png',
                        id: 3
                    },
                    {
                        sources: 'https://hcdn1.luffycity.com/static/frontend/index/banner11_1538122470.2779157.png',
                        id: 4
                    },
                    {
                        sources: 'https://hcdn1.luffycity.com/static/frontend/index/home-banner4_1535545832.4715614.png',
                        id: 5
                    },
                ]
            }
        }
    }


</script>

<style scoped>
 .banner_img {
            width: 100%;
            height: 480px;
        }
</style>
