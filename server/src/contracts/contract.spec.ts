import { ethers } from "ethers";
import { OGUOGU, ERC20, OGUOGU__factory, ERC20__factory } from ".";

describe("OGUOGU", () => {
  let provider: ethers.JsonRpcProvider;
  let operator: ethers.Wallet;
  let challenger: ethers.Wallet;

  let oguogu: OGUOGU;
  let usdt: ERC20;

  beforeAll(async () => {
    provider = new ethers.JsonRpcProvider("http://localhost:8545");
    operator = new ethers.Wallet(
        '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80', provider
    );
    challenger = new ethers.Wallet(
        '0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d', provider
    );

    oguogu = OGUOGU__factory.connect('0xdc64a140aa3e981100a9beca4e685f962f0cf6c9', provider);
    usdt = ERC20__factory.connect('0x5fbdb2315678afecb367f032d93f642f64180aa3', provider);
  });

  jest.setTimeout(30000);

  it('should deposit reward', async () => {
    
    const amount = ethers.parseUnits('10', 6);
    
    const tx0 = await usdt.connect(challenger).approve(oguogu.getAddress(), amount);
    await tx0.wait();

    const tx1 = await oguogu.connect(challenger).depositReward(challenger.address, amount)
    await tx1.wait();

    const balance = await oguogu.userReserves(challenger.address);
    expect(balance).toBe(amount);
  });
});
