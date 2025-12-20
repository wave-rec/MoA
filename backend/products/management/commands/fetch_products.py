from django.core.management.base import BaseCommand
from products.services.fss_api import fetch_products, upsert_products


class Command(BaseCommand):
    help = '금융감독원 API에서 예금/적금 상품 데이터 수집'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['deposit', 'savings', 'all'],
            default='all',
            help='수집할 상품 타입 (deposit: 예금만, savings: 적금만, all: 둘 다)'
        )

    def handle(self, *args, **options):
        product_type = options['type']
        
        self.stdout.write(self.style.WARNING(f'\n{product_type} 상품 데이터 수집 시작...\n'))

        try:
            # 예금 수집
            if product_type in ['deposit', 'all']:
                self.stdout.write('예금 상품 조회 중...')
                result = fetch_products('deposit')
                stats = upsert_products(result, 'deposit')
                self.stdout.write(
                    self.style.SUCCESS(
                        f'예금: {stats["products"]}개 상품, {stats["rates"]}개 금리 옵션 저장 완료'
                    )
                )

            # 적금 수집
            if product_type in ['savings', 'all']:
                self.stdout.write('\n적금 상품 조회 중...')
                result = fetch_products('savings')
                stats = upsert_products(result, 'savings')
                self.stdout.write(
                    self.style.SUCCESS(
                        f'적금: {stats["products"]}개 상품, {stats["rates"]}개 금리 옵션 저장 완료'
                    )
                )

            self.stdout.write(self.style.SUCCESS('\n데이터 수집 완료!\n'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n오류 발생: {str(e)}\n'))
            raise