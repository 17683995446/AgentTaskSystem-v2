"""
🌐 真实场景示例！
用 ContinuousAgent 做：
1. 实时数据监控
2. 定时数据采集
3. 健康检查
"""

import time
import random
from datetime import datetime
from continuous_agent import ContinuousAgent


class RealWorldAgent:
    """真实场景的 Agent"""
    
    def __init__(self):
        self.agent = ContinuousAgent()
        self.data_cache = []
        self.health_status = "ok"
        
    def setup_data_monitoring(self):
        """设置数据监控任务"""
        
        # 任务 1：每隔5秒采集一次数据
        def collect_data():
            # 模拟真实数据采集
            temperature = random.uniform(20, 30)
            humidity = random.uniform(40, 70)
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            data = {
                "time": timestamp,
                "temperature": round(temperature, 1),
                "humidity": round(humidity, 1)
            }
            
            self.data_cache.append(data)
            print(f"📊 采集数据: {data}")
            
            # 保持最近20条
            if len(self.data_cache) > 20:
                self.data_cache.pop(0)
                
            return data
        
        self.agent.add_scheduled_task("数据采集", 5, collect_data)
        
    def setup_health_check(self):
        """设置健康检查任务"""
        
        # 任务 2：一直运行的健康检查
        check_count = 0
        
        def health_check():
            nonlocal check_count
            check_count += 1
            
            # 模拟健康检查
            cpu_usage = random.uniform(10, 60)
            memory_usage = random.uniform(30, 80)
            
            status = "ok"
            if cpu_usage > 50:
                status = "warning"
            if memory_usage > 70:
                status = "critical"
            
            self.health_status = status
            
            print(f"❤️  健康检查 #{check_count}: CPU {cpu_usage:.1f}%, Mem {memory_usage:.1f}% - {status}")
            
            # 偶尔模拟失败
            if check_count % 5 == 0:
                raise Exception("模拟网络波动！")
                
            return status
        
        self.agent.add_loop_task("健康检查", health_check, max_retries=3)
        
    def setup_report_generator(self):
        """设置报告生成任务"""
        
        # 任务 3：每隔30秒生成报告
        def generate_report():
            if not self.data_cache:
                print("📝 暂无数据，跳过报告")
                return "no data"
            
            # 简单分析
            temps = [d["temperature"] for d in self.data_cache]
            avg_temp = sum(temps) / len(temps)
            
            report = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "data_points": len(self.data_cache),
                "avg_temperature": round(avg_temp, 1),
                "health_status": self.health_status
            }
            
            print(f"📈 生成报告: {report}")
            return report
        
        self.agent.add_scheduled_task("报告生成", 15, generate_report)
        
    def start(self, run_seconds: int = 30):
        """启动！"""
        print("\n" + "🌐"*30)
        print("  真实场景 - 数据监控系统")
        print("🌐"*30)
        
        self.setup_data_monitoring()
        self.setup_health_check()
        self.setup_report_generator()
        
        # 运行一段时间
        import asyncio
        
        async def run():
            task = asyncio.create_task(self.agent.start())
            await asyncio.sleep(run_seconds)
            self.agent.stop()
            await task
        
        asyncio.run(run())
        
        print("\n" + "="*60)
        print("  📊 运行总结")
        print("="*60)
        print(f"  共采集数据点: {len(self.data_cache)}")
        if self.data_cache:
            print(f"  最后数据: {self.data_cache[-1]}")
        print("="*60)


# ============================================
# 🚀 也可以直接用简单的方式
# ============================================

def quick_start_example():
    """快速开始 - 简单版本"""
    print("\n" + "🚀"*30)
    print("  快速开始 - 简单版本")
    print("🚀"*30)
    
    agent = ContinuousAgent()
    
    # 场景：每分钟检查一次网站
    def check_website():
        now = datetime.now().strftime("%H:%M:%S")
        # 模拟检查
        status = random.choice(["ok", "ok", "slow"])
        print(f"🌐 网站检查: {status} ({now})")
        return status
    
    agent.add_scheduled_task("网站监控", 3, check_website)
    
    # 场景：持续清理缓存
    def clear_cache():
        print("🧹 清理缓存...")
        # 模拟清理
        return "cache cleared"
    
    agent.add_scheduled_task("缓存清理", 8, clear_cache)
    
    # 启动
    import asyncio
    
    async def run():
        task = asyncio.create_task(agent.start())
        await asyncio.sleep(20)  # 运行20秒
        agent.stop()
        await task
    
    asyncio.run(run())


def main():
    print("\n" + "🎯"*30)
    print("  Agent 持续运行 - 真实场景演示")
    print("🎯"*30)
    
    # 运行真实场景
    real_agent = RealWorldAgent()
    real_agent.start(run_seconds=25)
    
    # 运行快速开始
    quick_start_example()
    
    print("\n" + "🎊"*30)
    print("  所有场景演示完成！")
    print("🎊"*30)


if __name__ == "__main__":
    main()
