import random
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from pandac.PandaModules import *
from PooledEffect import PooledEffect
from EffectController import EffectController

class VomitEffect(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/pir_t_efx_msc_vomit')
        if not VomitEffect.particleDummy:
            VomitEffect.particleDummy = render.attachNewNode(ModelNode('VomitEffectParticleDummy'))
            VomitEffect.particleDummy.setDepthWrite(0)
            VomitEffect.particleDummy.setFogOff()
            VomitEffect.particleDummy.setLightOff()
            VomitEffect.particleDummy.setColorScaleOff()
            VomitEffect.particleDummy.setTwoSided(1)
        self.f = ParticleEffect.ParticleEffect('VomitEffect')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereSurfaceEmitter')
        self.f.addParticles(self.p0)
        self.f0 = None
        self.setParticleOptions()
        return

    def setParticleOptions(self):
        if self.f0 != None:
            self.f.removeForceGroup(self.f0)
        self.f0 = ForceGroup.ForceGroup('gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -50.0), 1.0, 0)
        force0.setVectorMasks(1, 1, 1)
        force0.setActive(1)
        self.f0.addForce(force0)
        force1 = LinearJitterForce(15.0, 0)
        force1.setVectorMasks(1, 1, 1)
        force1.setActive(1)
        self.f0.addForce(force1)
        self.f.addForceGroup(self.f0)
        self.p0.setPoolSize(150)
        self.p0.setBirthRate(0.05)
        self.p0.setLitterSize(8)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(0)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.4)
        self.p0.factory.setLifespanSpread(0.05)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(20.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAUSER)
        self.p0.renderer.setUserAlpha(0.25)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.00035 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.00035 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.004 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.004 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, -6.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.125)
        return

    def createTrack(self):
        taskName = '%s-OrientEmitterTask' % self.__class__.__name__
        self.setParticleOptions()
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(1.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(0.7), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)