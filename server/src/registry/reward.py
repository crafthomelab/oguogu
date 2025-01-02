from src.database.repository import ChallengeRepository
from src.registry.transaction import TransactionManager


class ChallengeRewardService:
    
    def __init__(self, 
                 repository: ChallengeRepository,
                 transaction: TransactionManager):
        self.repository = repository
        self.transaction = transaction
        contract = transaction.oguogu_contract()
        self.complete_function = contract.functions.completeChallenge
        self.challenge_completed_event = contract.events.ChallengeCompleted()

    async def complete_challenge(
        self, 
        challenge_id: int
    ) -> str:
        """ 챌린지를 완료하고, 보상 트랜잭션을 지급합니다.
        """
        challenge = await self.repository.get_challenge_by_id(challenge_id)
        if not challenge.available_to_complete():
            raise ValueError("Challenge is not available to complete")
        request = self.complete_function(challenge.id)
                
        tx_receipt = await self.transaction.asend_transaction(request)
        tx_hash = tx_receipt['transactionHash'].to_0x_hex()
        
        events = await self.transaction.aget_events_from_transcation(
            tx_hash, 
            self.challenge_completed_event
        )
        complete_date = await self.transaction.aget_txreceipt_datetime(tx_receipt)
        for event in events:
            status = event['args']['status']
            payment_reward = event['args']['paymentReward']
            if status == 1:
                challenge.success(tx_hash, payment_reward, complete_date)
            else:
                challenge.fail(tx_hash, payment_reward, complete_date)
            await self.repository.complete_challenge(challenge)
        return tx_hash
        